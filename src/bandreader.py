import numpy as np
import pandas as pd
from datetime import datetime


class HeartRateBand:
    """Provides basic functions to extract heart beat rate from the given path.
    Heart beat rates are acquired with Microsoft Band and custom Android app."""

    def __init__(self, path, ident):
        """
        :param path: (str) Path to a files
        :param ident: (str) User identifier
        """
        self.path = path
        self.ident = ident

    def load(self):
        """Parse and return time of acquired HR and HR value for this time."""
        data = pd.read_csv(self.path+self.ident+'.txt', sep=';|,', engine='python')
        data = data.dropna(axis=1, how='all')

        date_time, rate = data.iloc[:, 0], data.iloc[:, 1]
        rate = rate.tolist()
        date_time = [convert_to_epoch(i) for i in date_time]

        return [np.array(date_time), np.array(rate)]


def convert_to_epoch(value):
    """Converts to Unix epoch time format"""
    datetime_object = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return int(datetime_object.timestamp()) * 1000 + int(datetime_object.microsecond / 1000)
