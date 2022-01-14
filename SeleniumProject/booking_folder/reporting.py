import pandas as pd

class Reporting():
    def __init__(self, name, price, rating, location):
        self.name = name
        self.price = price
        self.rating = rating
        self.location = location

    def __str__(self):
        print(f'{self.name},{self.price},{self.rating},{self.location}')