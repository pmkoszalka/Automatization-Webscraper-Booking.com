"""This file contains filtration for booking.com"""

# import
from selenium.webdriver.remote.webdriver import WebDriver

class BookingFiltration:
    """Applies filtration to post-search booking website"""

    def __init__(self, driver: WebDriver):
        self.driver = driver  # allows to find elements on page

    def apply_star_rating(self, *star_values):
        """Sorts hotels by number of stars"""

        star_filtration_box = self.driver.find_element_by_css_selector('div[data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements_by_css_selector('*')

        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':  # looks for text
                    star_element.click()

    def sort_price_lowest_first(self):
        """Sorts by lowest the price"""

        price_lowest_first = self.driver.find_element_by_css_selector('li[data-id="price"]')
        price_lowest_first.click()

    def sort_best_reviewed_lowest_price(self):
        """Sorts by best reviews and lowest price"""

        best_reviews_lowest_price = self.driver.find_element_by_css_selector('li[data-id="review_score_and_price"]')
        best_reviews_lowest_price.click()