from codecs import backslashreplace_errors
from doctest import master
from locale import currency
import constants as keys
from kucoin.user import user
from kucoin.market import market
import pandas as pd


api_key = keys.api_key
api_secret = keys.api_secret
api_passphrase = keys.api_passphrase

user = user.UserData(key = api_key, secret = api_secret, passphrase = api_passphrase)
all_accounts = user.get_account_list()
all_accounts = pd.DataFrame.from_dict(all_accounts)
all_accounts = all_accounts.drop(['id', 'type', 'available', 'holds'], axis=1)

market = market.MarketData(url='https://api.kucoin.com' )
fiat_prices = market.get_fiat_price()
fiat_prices = pd.DataFrame(fiat_prices.items(), columns=['currency', 'price'])
# print(fiat_prices.head(10))

masterDF = all_accounts.merge(fiat_prices, on='currency')
masterDF['balance'] = pd.to_numeric(masterDF['balance'])
masterDF['price'] = pd.to_numeric(masterDF['price'])
masterDF['value'] = masterDF['balance'] * masterDF['price']
masterDF['value'].round(2)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
masterDF = masterDF.drop(masterDF[masterDF.value < 5].index)
totalBalance = masterDF['value'].sum()
print(masterDF.head(10))
print(round(totalBalance,2))