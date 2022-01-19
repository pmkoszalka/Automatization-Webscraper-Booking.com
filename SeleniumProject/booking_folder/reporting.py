"""This file contains the logic for reporting the data"""

# import
import pandas as pd

class Reporting():
    """Reports the data"""

    _dataframe_dictionary = {'Hotel Name': [], 'Price': [], 'Location': [], 'Rating': []}

    def __init__(self, name, price, rating, location):

        # sets up the basic info of a hotel entry
        self.name = name
        self.price = price
        self.location = location
        self.rating = rating

        # sets up the the dataframe_dictionary for the dataframe
        Reporting._dataframe_dictionary['Hotel Name'].append(self.name)
        Reporting._dataframe_dictionary['Price'].append(self.price)
        Reporting._dataframe_dictionary['Location'].append(self.location)
        Reporting._dataframe_dictionary['Rating'].append(self.rating)

    @staticmethod
    def create_dataframe():
        """Creates a dataframe from tje dataframe_dictionary"""

        df = pd.DataFrame(Reporting._dataframe_dictionary)

        return df

    def __str__(self):
        """Prints out the data entries"""

        return f'Reporting({self.name}, {self.price},  {self.location}, {self.rating})'
