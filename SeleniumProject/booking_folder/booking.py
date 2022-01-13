"""This file contains main class and functions to perform basic automation and scraping of booking.com"""

# imports
import numpy
from selenium import webdriver
import datetime
from Selenium.SeleniumProject.booking_folder.booking_filtration import BookingFiltration
from Selenium.SeleniumProject.booking_folder import constants as const
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import re
import os

# setting pandas properties
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: '%.2f' % x)


class Booking(webdriver.Chrome):
    """Allows to perform basic automation and data scraping of booking.com"""

    def __init__(self, driver_path=const.CWD, teardown=True):
        self.driver_path = driver_path  # sets the path to our webdriver
        self.teardown = teardown  # allows to quit browser after we are done
        os.environ['PATH'] += os.pathsep + driver_path  # adds path to environmental variables
        options = webdriver.ChromeOptions()  # creates instance of ChromeOptions
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # disables the info-bar
        super(Booking, self).__init__(options=options) # allows us to avoid using the base class name explicitly
        self.implicitly_wait(15)  # polls the DOM for 15 sec while trying to find an element
        self.maximize_window() # maximizes the Chrome window
        self.__visitors_numbers = 0  # stores visitors number, helps to create ratio column
        self.__nights_spent = 0  # stores nights spent number, helps to create ratio column

    def land_first_page(self):
        """Opens booking.com"""

        self.get(const.BASE_URL)


    def close_pop_up(self):
        """Closes the pop up"""

        pop_up_close = self.find_element_by_id("onetrust-accept-btn-handler")
        pop_up_close.click()

    def change_language_to_english(self):
        """Changes the language for the site to English"""

        language_panel = self.find_element_by_class_name('bui-avatar__image')
        language_panel.click()

        language_to_english = self.find_element_by_xpath("//*[contains(text(), 'English (UK)')]")
        language_to_english.click()

    def change_currency(self, currency=None):
        """Changes the currency"""

        currency_element = self.find_element_by_css_selector('button[data-tooltip-text="Choose your currency"]')
        currency_element.click()
        selected_currency_element = self.find_element_by_css_selector(
            'a[data-modal-header-async-url-param*="selected_currency={}"]'.format(currency)
        )
        selected_currency_element.click()

    def input_travel_location(self, destination):
        """Selects travel destination"""

        search_bar = self.find_element_by_id('ss')
        search_bar.clear()
        search_bar.send_keys(destination)
        first_result = self.find_element_by_css_selector('li[data-i="0"]')
        first_result.click()

    def select_date(self, check_in_date, check_out_date):
        """Selects check in and check out dates"""

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
        """Selects certain number of adults in a Booking search"""

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
        """Finds and clicks the search button"""

        search_button = self.find_element_by_css_selector('button[class="sb-searchbox__button "]')
        search_button.click()

    def apply_filtration(self):
        """Applies filtration to the Booking site"""

        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        # filtration.sort_price_lowest_first()

    def stops(self):
        """"""
        # waits for the elements to load on the domain
        wait = WebDriverWait(self, 500)
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

    def report_hotel_names(self, data_entries_number=25):
        """Reports selected number of hotel deals"""

        # creating variables
        table_hotel_info = pd.DataFrame(columns=['Hotel Name', 'Price', 'Location', 'Rating'])
        page_number = 1

        # setting up the loop for getting data
        while data_entries_number > len(table_hotel_info):

            # placeholders
            hotel_names = []
            hotel_prices = []
            hotel_ratings = []
            locations = []

            deals = self.find_elements_by_css_selector('div[data-testid="property-card"]')

            for deal in deals:

                # get hotel names
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

                # get hotel price
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

                # get hotel location
                try:
                    location = deal.find_element_by_css_selector('span[data-testid="distance"]').get_attribute(
                        'innerHTML'
                    ).strip()
                    locations.append(location)
                except:
                    # print('No location')
                    locations.append('No location')
                    continue

                # get hotel rating
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

            # creating and merging dataframes
            hotels_info = [(a, b, c, d) for a, b, c, d in zip(hotel_names, hotel_prices, locations, hotel_ratings)]
            hotels_info_df = pd.DataFrame(hotels_info, columns=['Hotel Name', 'Price', 'Location', 'Rating'])
            table_hotel_info = table_hotel_info.append(hotels_info_df, ignore_index=True)

            # checking if the next page needs to be clicked
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
    def __data_cleaning_func(text: str):
        """Extracts number from a string"""

        try:
            text = text.replace(' ', '').replace(',', '')
            text = float(re.findall('[0-9.]+', str(text))[0])
        except:
            text = numpy.nan
        return text

    @staticmethod
    def data_cleaning(data: pd.DataFrame):
        """Cleans the data of "Price", "Location" and "Rating" columns"""

        data['Price'] = data['Price'].apply(Booking.__data_cleaning_func)
        data['Location'] = data['Location'].apply(Booking.__data_cleaning_func)
        data['Rating'] = data['Rating'].apply(Booking.__data_cleaning_func)
        return data

    @staticmethod
    def show_basic_stats(data_cleaned: pd.DataFrame):
        """Creates basic statistics for data"""
        return data_cleaned.describe()

    def add_ratio_column(self, data_cleaned):
        """Adds "Price_per_nights_per_visitors" column to the dataframe"""

        data_cleaned['Price_per_nights_per_visitors'] = data_cleaned['Price'] / (
                    self.__visitors_numbers * self.__nights_spent)
        return data_cleaned


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Quits the browser if teardown is set to True"""

        if self.teardown:
            self.implicitly_wait(5)
            self.quit()
