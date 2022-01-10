# this file will describe the methods
import numpy
from selenium import webdriver
import os
import datetime
from Selenium.booking_folder.booking_filtration import BookingFiltration
from Selenium.booking_folder import constants as const
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import re

# Setting pandas properties
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: '%.2f' % x)


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r'C:\Users\pmkos\PycharmProjects\pythonProject\Selenium\booking_folder', teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += os.pathsep + driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
        self.__visitors_numbers = 0
        self.__nights_spent = 0

    def land_first_page(self):
        self.get(const.BASE_URL)  # this will probably won't change
        self.implicitly_wait(5)

        pop_up_close = self.find_element_by_id("onetrust-accept-btn-handler")
        pop_up_close.click()
        self.implicitly_wait(5)

        language_panel = self.find_element_by_class_name('bui-avatar__image')
        language_panel.click()
        self.implicitly_wait(5)

        language_to_english = self.find_element_by_xpath("//*[contains(text(), 'English (UK)')]")
        language_to_english.click()

    def change_currency(self, currency=None):
        currency_element = self.find_element_by_css_selector('button[data-tooltip-text="Choose your currency"]')
        currency_element.click()
        selected_currency_element = self.find_element_by_css_selector(
            'a[data-modal-header-async-url-param*="selected_currency={}"]'.format(currency)
        )
        selected_currency_element.click()

    def input_travel_location(self, location):
        search_bar = self.find_element_by_id('ss')
        search_bar.clear()
        search_bar.send_keys(location)
        first_result = self.find_element_by_css_selector('li[data-i="0"]')
        first_result.click()

    def select_date(self, check_in_date, check_out_date):

        # definitions for check in
        check_in_date_obj = datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
        check_in_year = check_in_date_obj.year
        check_in_month = check_in_date_obj.month
        check_in_number_months = check_in_year * 12 + check_in_month
        check_in_difference = check_in_number_months - const.TODAY_NUMBER_MONTHS

        # definitions for check out
        check_out_date_obj = datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
        check_out_year = check_out_date_obj.year
        check_out_month = check_out_date_obj.month
        check_out_number_months = check_out_year * 12 + check_out_month
        check_out_difference = check_out_number_months - check_in_number_months

        # making sure that check out and check in dates are not 45 days apart
        check_out_check_in_difference = check_out_date_obj - check_in_date_obj
        check_out_check_in_difference = check_out_check_in_difference.days

        self.__nights_spent = check_out_check_in_difference

        assert check_out_check_in_difference < 46, 'Reservations for more than 45 nights are not possible!'

        # logic for check in
        if check_in_difference == 0 or check_in_difference == 1:
            check_in_date = self.find_element_by_css_selector(f'td[data-date="{check_in_date}"]')
            check_in_date.click()

        elif check_in_difference > 1:
            next_month = self.find_element_by_css_selector('div[data-bui-ref="calendar-next"]')

            for click in range(check_in_difference):
                next_month.click()

            check_in_date = self.find_element_by_css_selector(f'td[data-date="{check_in_date}"]')
            check_in_date.click()

        else:
            raise Exception('Input future date!')

        # logic for check out
        if check_out_difference == 0 or check_out_difference == 1:
            check_out_date = self.find_element_by_css_selector(f'td[data-date="{check_out_date}"]')
            check_out_date.click()

        elif check_out_difference > 1:
            next_month = self.find_element_by_css_selector('div[data-bui-ref="calendar-next"]')

            for click in range(check_out_difference):
                next_month.click()

            check_out_date = self.find_element_by_css_selector(f'td[data-date="{check_out_date}"]')
            check_out_date.click()

        else:
            raise Exception('Input future date!')

    def select_adults_number(self, adults_number=2):
        select_bar = self.find_element_by_id("xp__guests__toggle")
        select_bar.click()
        self.__visitors_numbers = adults_number

        if adults_number < 2:
            adults_button_decrease = self.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            )
            adults_button_decrease.click()

        elif adults_number == 2:
            pass

        else:
            for click in range(adults_number - 2):
                adults_button_increase = self.find_element_by_css_selector(
                    'button[aria-label="Increase number of Adults"]')
                adults_button_increase.click()

    def search(self):
        search_button = self.find_element_by_css_selector('button[class="sb-searchbox__button "]')
        search_button.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        # filtration.sort_price_lowest_first()

    def report_hotel_names(self, data_entries_number=25):

        # Creating variables
        table_hotel_info = pd.DataFrame(columns=['Hotel Name', 'Price', 'Location', 'Rating'])
        page_number = 1
        wait = WebDriverWait(self, 500)

        # setting up the loop for getting data
        while data_entries_number > len(table_hotel_info):
            self.get(self.current_url)
            time.sleep(5)

            element_card = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="property-card"]')))
            element_title = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="title"]')))
            element_price = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="price-and-discounted-price"]')))
            element_location = wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-testid="distance"]')))
            element_rating = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="review-score"]')))

            hotel_names = []
            hotel_prices = []
            hotel_ratings = []
            locations = []

            deals = self.find_elements_by_css_selector('div[data-testid="property-card"]')

            for deal in deals:

                # Get hotel names
                try:
                    hotel_name = deal.find_element_by_css_selector(
                        'div[data-testid="title"]'
                    ).text
                    hotel_names.append(hotel_name)
                    # print(hotel_name)
                except:
                    hotel_names.append('No Name')
                    # print('No name')
                    continue

                # Get hotel price
                try:
                    hotel_price = deal.find_element_by_css_selector(
                        'div[data-testid="price-and-discounted-price"]').find_elements_by_tag_name("span")[
                        -1].get_attribute(
                        'innerHTML'
                    ).strip()
                    hotel_price = hotel_price.replace('&nbsp;', ' ')
                    hotel_prices.append(hotel_price)
                    # print(hotel_price)
                except:
                    # print('no price')
                    hotel_prices.append('No price')
                    continue

                # Get hotel location
                try:
                    location = deal.find_element_by_css_selector('span[data-testid="distance"]').get_attribute(
                        'innerHTML'
                    ).strip()
                    locations.append(location)
                except:
                    # print('No location')
                    locations.append('No location')
                    continue

                # Get hotel rating
                try:
                    hotel_rating = deal.find_element_by_css_selector(
                        'div[data-testid="review-score"]'
                    ).find_element_by_tag_name("div").get_attribute('innerHTML').strip()
                    hotel_ratings.append(hotel_rating)
                    # print(hotel_rating)
                except:
                    # print('no rating')
                    hotel_ratings.append("No rating")
                    continue

            # Creating and merging dataframes
            hotels_info = [(a, b, c, d) for a, b, c, d in zip(hotel_names, hotel_prices, locations, hotel_ratings)]
            hotels_info_df = pd.DataFrame(hotels_info, columns=['Hotel Name', 'Price', 'Location', 'Rating'])
            table_hotel_info = table_hotel_info.append(hotels_info_df, ignore_index=True)

            # Checking if the next page needs to be clicked
            if data_entries_number > len(table_hotel_info):
                try:
                    page_number = page_number + 1
                    button_page = self.find_element_by_css_selector(f'button[aria-label=" {page_number}"]')
                    button_page.click()
                except:
                    print(f'There are only {len(table_hotel_info)} properties listed!')
                    break

        return table_hotel_info.iloc[:data_entries_number, :]

    @staticmethod
    def __data_cleaning_func(text : str):
        try:
            text = text.replace(' ', '').replace(',', '')
            text = float(re.findall('[0-9.]+', str(text))[0])
        except:
            text = numpy.nan
        return text

    #@staticmethod
    def __data_cleaning(self, data : pd.DataFrame):
        data['Price'] = data['Price'].apply(Booking.__data_cleaning_func)
        data['Location'] = data['Location'].apply(Booking.__data_cleaning_func)
        data['Rating'] = data['Rating'].apply(Booking.__data_cleaning_func)
        data['Price_per_nights_per_visitors'] = data['Price'] / (self.__visitors_numbers * self.__nights_spent)
        return data

    # def __price_per_nights_per_visitors(self, data: pd.DataFrame):
    #     Booking.__data_cleaning(data)
    #     data['Price_per_nights_per_visitors'] = data['Price'] / (self.__visitors_numbers * self.__nights_spent)
    #     return data

    @staticmethod
    def show_basic_stats(data : pd.DataFrame):
        # Booking.__price_per_nights_per_visitors(data)
        return Booking.__data_cleaning(data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.implicitly_wait(5)
            self.quit()  # this methods shuts down chromes browser
