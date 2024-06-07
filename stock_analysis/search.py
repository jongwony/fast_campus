import meilisearch
import pandas as pd

client = meilisearch.Client('http://localhost:7700', 'aSampleMasterKey')


def bootstrap_stocks():
    """
    https://www.nasdaq.com/market-activity/stocks/screener
    """
    # json.dumps(body)[1919-30:1919+30]
    stocks = pd.read_csv('nasdaq_screener.csv', na_filter=False)
    # df[df['Symbol'].str.contains(r'[^\w]', regex=True)]
    stocks['id'] = stocks['Symbol'].str.strip().replace(r'[/^]', '_', regex=True)
    client.index('stocks').add_documents(stocks.to_dict(orient='records'), primary_key='id')


def stock_search(query):
    return client.index('stocks').search(query)


def delete_stocks():
    client.delete_index('stocks')


if __name__ == '__main__':
    delete_stocks()
    bootstrap_stocks()
