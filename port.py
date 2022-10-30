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

def getPort():
    all_accounts = user.get_account_list()
    all_accounts = pd.DataFrame.from_dict(all_accounts)
    all_accounts = all_accounts.drop(['id', 'type', 'available', 'holds'], axis=1)

    fiat_prices = market.get_fiat_price()
    fiat_prices = pd.DataFrame(fiat_prices.items(), columns=['currency', 'price'])
    # print(fiat_prices.head(10))

    masterDF = all_accounts.merge(fiat_prices, on='currency')
    masterDF['balance'] = masterDF['balance'].astype(float).round(2)
    masterDF['price'] = masterDF['price'].astype(float).round(5)
    masterDF['value'] = (masterDF['balance'] * masterDF['price']).astype(float).round(2)
    masterDF = masterDF.drop(masterDF[masterDF.value < 5].index)
    totalBalance = masterDF['value'].sum().round(2)
    totalBalanceList = [totalBalance]

    # print(masterDF.head(10))
    # print(round(totalBalance,2))
    masterDF = masterDF.reset_index(drop=True)

    response = ""
    # response += f"{'CURRENCY' : <12}{'BALANCE' : <12}{'PRICE' : <12}{'$ VALUE' : <12}\n"
    # response += "\n"
    # response += masterDF.to_string(col_space=12, index=False, header=False, justify='left')
    # response += "\n\n"
    # response += "Total Balance = ${}".format(round(totalBalance,2))
    response += tabulate(masterDF, headers=["", "Currency", "Balance", "Price", "$ Value"], tablefmt='pretty',showindex=False)
    response += "\n\n"
    response += tabulate([totalBalanceList], ["TOTAL BALANCE"], tablefmt="pretty")

    return response

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
      if df.empty:
        string = f"Price info for {ticker} unavailable."
        response += string
        return response
      else:
        response += tabulate(df, headers=["Currency", "Price"], tablefmt='pretty',showindex=False)
        return response