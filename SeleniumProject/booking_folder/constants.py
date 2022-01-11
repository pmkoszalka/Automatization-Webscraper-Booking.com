"""Stores constants"""

# imports
from datetime import date
import os

#constants
CWD = os.path.dirname(os.path.realpath(__file__))
BASE_URL = "https://www.booking.com"
TODAY_DATE = date.today()
TODAY_YEAR = TODAY_DATE.year
TODAY_MONTH = TODAY_DATE.month
TODAY_NUMBER_MONTHS = TODAY_YEAR * 12 + TODAY_MONTH