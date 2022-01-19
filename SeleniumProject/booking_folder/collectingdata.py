"""This file contains the data collection logic"""

# imports
from Selenium.SeleniumProject.booking_folder.reporting import Reporting
from selenium.webdriver.remote.webdriver import WebDriver

class CollectingData:
    """Collects the data from a booking page"""

    def __init__(self, driver: WebDriver):
        self.driver = driver  # allows to find elements on page
        self.driver.implicitly_wait(30)  # polls the DOM for 30 sec while trying to find an element

    def gather_data(self):
        """Gathers the data from the page and sets up the reporting"""

        self.driver.refresh()  # refresh is crucial for data to be loaded properly
        deals = self.driver.find_elements_by_css_selector('div[data-testid="property-card"]')

        for deal in deals:
            # gathers the hotel names
            try:
                hotel_name = deal.find_element_by_css_selector(
                    'div[data-testid="title"]'
                ).text
            except:
                hotel_name = 'No Name'
                continue

            # gathers the hotel price
            try:
                hotel_price = deal.find_element_by_css_selector(
                    'div[data-testid="price-and-discounted-price"]').find_elements_by_tag_name("span")[
                    -1].text
            except:
                hotel_price = 'No price'
                continue

            # gathers the hotel location
            try:
                location = deal.find_element_by_css_selector('span[data-testid="distance"]').text
            except:
                location = 'No location'
                continue

            # gathers the hotel rating
            try:
                hotel_rating = deal.find_element_by_css_selector(
                    'div[data-testid="review-score"]'
                ).find_element_by_tag_name("div").text
            except:
                hotel_rating = "No rating"
                continue

            # sets up the Reporting class for data to be properly reported
            hotel = Reporting(hotel_name, hotel_price, hotel_rating, location)
