from tarfile import NUL
from urllib import response
import constants as keys
from kucoin.user import user
from kucoin.market import market
import pandas as pd
from tabulate import tabulate

api_key = keys.api_key
api_secret = keys.api_secret
api_passphrase = keys.api_passphrase

user = user.UserData(key = api_key, secret = api_secret, passphrase = api_passphrase)
market = market.MarketData(url='https://api.kucoin.com' )

def getPrice(ticker = None):
    fiat_prices = market.get_fiat_price()
    fiat_prices = pd.DataFrame(fiat_prices.items(), columns=['currency', 'price'])
    # fiat_prices = fiat_prices.reset_index(drop=True)
    # print(fiat_prices.head(10))
    # print(ticker)
    response = ""

    if ticker == None:
        # print(fiat_prices.head(10))
        df = fiat_prices[fiat_prices['currency'].isin(['BTC', 'ETH'])]
        response += tabulate(df, headers=["Currency", "Price"], tablefmt='pretty',showindex=False)
        return response
    else:
        df = fiat_prices[fiat_prices['currency'] == ticker]
        df = df.reset_index(drop=True)
        # print(df.head(1))
        response += tabulate(df, headers=["Currency", "Price"], tablefmt='pretty',showindex=False)
        return response

ticker = 'AUDIO'
print(getPrice())
print(getPrice(ticker))