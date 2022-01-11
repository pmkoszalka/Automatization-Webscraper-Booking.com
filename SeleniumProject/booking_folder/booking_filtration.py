"""This file includes a class with instance methods
that is responsible for interaction automatization
and data scraping of booking.com"""

#imports
from selenium.webdriver.remote.webdriver import WebDriver
import time

class BookingFiltration:
    """Applies filtration to post-search booking website"""
    def __init__(self, driver: WebDriver):
        self.driver = driver  # allows to find elements on page

    def apply_star_rating(self, *star_values):
        """Sorts hotels by number of stars"""
        star_filtration_box = self.driver.find_element_by_css_selector('div[data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements_by_css_selector('*')  # this lookts for every child selector

        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':  # looks for text
                    star_element.click()

    def sort_price_lowest_first(self):
        """Sorts by lowest the price"""
        price_lowest_first = self.driver.find_element_by_css_selector('li[data-id="price"]')
        price_lowest_first.click()