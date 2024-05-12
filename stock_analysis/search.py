import meilisearch
import pandas as pd

client = meilisearch.Client('http://localhost:7700', 'aSampleMasterKey')


def bootstrap_stocks():
    # https://www.nasdaqtrader.com/Trader.aspx?id=symbollookup
    stocks = pd.read_csv('nasdaqlisted.txt', sep='|')
    stocks.reset_index(names='id', inplace=True)
    stocks.replace(pd.NA, None, inplace=True)
    stocks = stocks[['id', 'Symbol', 'Security Name']].to_dict(orient='records')
    client.index('stocks').add_documents(stocks)


def stock_search(query):
    return client.index('stocks').search(query)
