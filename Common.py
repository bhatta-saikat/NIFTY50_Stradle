import requests
import pandas as pd


LOT = 5
SYMBOL = 'NIFTY'
ORDER_TYPE ='INTRADAY'
Gap = 200
qty = 50*LOT
transType = 'SELL'
CommonSymbol = 'NIFTY25APR24'
StrikeRange = 1500
PE_Primium  = 40
CE_Primium = 40


url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry']).apply(lambda x: x.date())
token_df

#Saving Data
token_df.to_csv('token_df.csv')

closingTime = int(23) * 60 + int(59)
orderPlaceTime = int(0) * 60 + int(39)
TradeTime = int(0) * 60 + int(30)