import pandas as pd

class Reporting():
    _dicto = {'Hotel Name': [], 'Price': [], 'Location': [], 'Rating': []}

    def __init__(self, name, price, rating, location):
        self.name = name
        self.price = price
        self.location = location
        self.rating = rating
        Reporting._dicto['Hotel Name'].append(self.name)
        Reporting._dicto['Price'].append(self.price)
        Reporting._dicto['Location'].append(self.location)
        Reporting._dicto['Rating'].append(self.rating)

    @staticmethod
    def create_dataframe():
        df = pd.DataFrame(Reporting._dicto)
        return df

    def __str__(self):
        return f'Reporting({self.name}, {self.price},  {self.location}, {self.rating})'
