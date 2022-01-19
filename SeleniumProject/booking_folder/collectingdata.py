from Selenium.SeleniumProject.booking_folder.reporting import Reporting
from selenium.webdriver.remote.webdriver import WebDriver

class CollectingData:

    def __init__(self, driver: WebDriver):
        self.driver = driver  # allows to find elements on page
        self.driver.implicitly_wait(30)

    def gather_data(self):
        """Reports selected number of hotel deals"""
        self.driver.refresh()
        deals = self.driver.find_elements_by_css_selector('div[data-testid="property-card"]')

        for deal in deals:
            # get hotel names
            try:
                hotel_name = deal.find_element_by_css_selector(
                    'div[data-testid="title"]'
                ).text
            except:
                hotel_name = 'No Name'
                continue

            # get hotel price
            try:
                hotel_price = deal.find_element_by_css_selector(
                    'div[data-testid="price-and-discounted-price"]').find_elements_by_tag_name("span")[
                    -1].text
            except:
                hotel_price = 'No price'
                continue

            # get hotel location
            try:
                location = deal.find_element_by_css_selector('span[data-testid="distance"]').text
            except:
                location = 'No location'
                continue

            # get hotel rating
            try:
                hotel_rating = deal.find_element_by_css_selector(
                    'div[data-testid="review-score"]'
                ).find_element_by_tag_name("div").text
            except:
                hotel_rating = "No rating"
                continue

            hotel = Reporting(hotel_name, hotel_price, hotel_rating, location)
