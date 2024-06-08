import pandas as pd


def load_data():
    return pd.read_csv('winemag-data-130k-v2.csv')


def get_country_stats(data):
    return data['country'].value_counts()
