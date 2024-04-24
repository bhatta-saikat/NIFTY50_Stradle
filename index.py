import Angel
import Fyers
import Common
import json
import requests
import time
import pyotp
import os
import requests
from urllib.parse import parse_qs,urlparse
import sys
import warnings
warnings.filterwarnings('ignore')
import pandas_ta as ta
from fyers_api import fyersModel, accessToken
from datetime import datetime, timedelta
import time
import os
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt  # Import Matplotlib



#st.title("BANKNIFTY Algo Based Trading")
st.subheader("Option Strategy Window")
Optx_Symbol = st.sidebar.text_input("Symbol:",value= "NIFTY")
Expiry = st.sidebar.text_input("Expiry-Date-Calculation:",value='0')
CE_Primium = st.sidebar.text_input("CE-Premium:",value='20')
PE_Primium = st.sidebar.text_input("PE-Premium:",value='20')
qty = st.sidebar.text_input("Choose-Trade-Qty:",value='100')
OrderPlace_Hour = st.sidebar.text_input("Order-Place-Hour:",value ="9")
OrderPlace_Min = st.sidebar.text_input("Order-Place-Min:",value = "47")

Text1 = text_placeholder = st.empty()
Text2 = text_placeholder = st.empty()
Text3 = text_placeholder = st.empty()
Text4 = text_placeholder = st.empty()
Text5 = text_placeholder = st.empty()
Text6 = text_placeholder = st.empty()

Text7 = text_placeholder = st.empty()
Data1 = df_placeholder = st.empty()

Text8 = text_placeholder = st.empty()
Data2 = df_placeholder = st.empty()

st.subheader("NSE-Option-Chain Analysis")
Data3 = df_placeholder = st.empty()

Text9 = text_placeholder = st.empty()

st.subheader(f"{Optx_Symbol}-Chart Data Analysis")
# Placeholder for chart
Chart =chart_placeholder = st.empty()
st.subheader(f"{Optx_Symbol}-PNL-Data Analysis:")
Text15 = text_placeholder = st.empty()
Text16 = text_placeholder = st.empty()
Text17 = text_placeholder = st.empty()
Data4 = df_placeholder = st.empty()
Text10 = text_placeholder = st.empty()
Text11 = text_placeholder = st.empty()
Text12 = text_placeholder = st.empty()
Text13 = text_placeholder = st.empty()
Text14 = text_placeholder = st.empty()

orderPlaceTime = int(OrderPlace_Hour) * 60 + int(OrderPlace_Min)
#Text5.text(f"{orderPlaceTime}")
orderPlaceTime = Common.orderPlaceTime
TradeTime = Common.TradeTime
interval = 30
SYMBOL = Optx_Symbol
StrikeRange = Common.StrikeRange
#CommonSymbol = Common.CommonSymbol
token_df = pd.read_csv('token_df.csv')
timeNow = (datetime.datetime.now().hour*60 + datetime.datetime.now().minute)

def getTime():
    return datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
localtime = time.localtime()

def check_Common():
    token_df = pd.read_csv('token_df.csv')
    #FIND RECENT EXP DATE
    spotSymInfo = token_df[(token_df.symbol == SYMBOL) & (token_df.exch_seg == 'NSE')].iloc[0].to_dict()
    # print(f'spotSymInfo : {spotSymInfo}')
    token_df = token_df.astype({'strike': float})
    expiryList = token_df[(token_df.name == SYMBOL) & (token_df.instrumenttype == 'OPTIDX')]['expiry'].unique().tolist()
    expiryList.sort()
    recentExpiry = expiryList[int(Expiry)]
    Text2.text(f"{Optx_Symbol}-Respective Expiry Date = {recentExpiry}")

    txt = recentExpiry
    x = txt.split('-')
    print(x[0])
    print(x[1])
    print(x[2])

    txt = x[0]
    y = txt.split('20')

    print(y[1])

    if x[1]=='01':
            CommonSymbol = f"{Optx_Symbol}{x[2]}JAN{y[1]}"

    if x[1]=='02':
        CommonSymbol = f"{Optx_Symbol}{x[2]}FEB{y[1]}" 

    if x[1]=='03':
        CommonSymbol = f"{Optx_Symbol}{x[2]}MAR{y[1]}"

    if x[1]=='04':
        CommonSymbol = f"{Optx_Symbol}{x[2]}APR{y[1]}"  

    if x[1]=='05':
        CommonSymbol = f"{Optx_Symbol}{x[2]}MAY{y[1]}"

    if x[1]=='06':
        CommonSymbol = f"{Optx_Symbol}{x[2]}JUN{y[1]}" 

    if x[1]=='07':
        CommonSymbol = f"{Optx_Symbol}{x[2]}JUL{y[1]}"

    if x[1]=='08':
        CommonSymbol = f"{Optx_Symbol}{x[2]}AUG{y[1]}" 

    if x[1]=='09':
        CommonSymbol = f"{Optx_Symbol}{x[2]}SEP{y[1]}"

    if x[1]=='10':
        CommonSymbol = f"{Optx_Symbol}{x[2]}OCT{y[1]}" 

    if x[1]=='11':
        CommonSymbol = f"{Optx_Symbol}{x[2]}NOV{y[1]}"

    if x[1]=='12':
        CommonSymbol = f"{Optx_Symbol}{x[2]}DEC{y[1]}"     

    Text3.text(f"The Common Symbol For = {CommonSymbol}")


    #FIND NIFTY50 LTP
    ltpInfo = Angel.obj.ltpData('NSE', spotSymInfo['symbol'], spotSymInfo['token'])
    indexLtp = ltpInfo['data']['ltp']
    yesterDay = ltpInfo['data']['close']
    Change = round((indexLtp - yesterDay),2)

    print(f'NIFTY50 Spot Ltp : {indexLtp}')
    atmStrike = round(int(indexLtp) / 50) * 50
    print(f'Spot Value : {atmStrike}')
    Range = int((StrikeRange) / 25 + 1)
    infos = []
    ATM_Strike = atmStrike
    #CE_Strike = atmStrike + int(GAP)
    #PE_Strike =  atmStrike - int(GAP)

    Text4.text(f"{Optx_Symbol}-LTP is = {indexLtp}")
    Text5.text(f"{Optx_Symbol}-Changed Price is = {Change}")
    Text6.text(f"{Optx_Symbol}-SPOT-VALUE is = {ATM_Strike}")


    for i in range(Range):
        symbolDf = token_df[(token_df.name == SYMBOL) & (token_df.expiry == recentExpiry) & (token_df.instrumenttype == 'OPTIDX')]
        Strike = ATM_Strike - StrikeRange
        # print(Strike)
        StrikeSymbol = f'{CommonSymbol}{Strike}PE'
        df = symbolDf[(symbolDf['symbol'] == StrikeSymbol)]
        StrikeToken = df['token'].iloc[0]
        # print(StrikeSymbol)
        ltpInfo = Angel.obj.ltpData('NFO', StrikeSymbol, StrikeToken)

        Ltp = ltpInfo['data']['ltp']
        Token = ltpInfo['data']['symboltoken']
        Symbol = ltpInfo['data']['tradingsymbol']

        lst = [Symbol, Token, Ltp]
        dframe = pd.DataFrame(lst)
        df = dframe.T
        df = df.rename({0: 'Symbol', 1: 'Token', 2: 'LTP'}, axis=1)
        df['Strike'] = Strike
        infos.append(df)
        ATM_Strike = ATM_Strike + 50

        PE_Data = pd.DataFrame(np.concatenate(infos))
        PE_Data = PE_Data.rename({0: 'Symbol', 1: 'Token', 2: 'LTP', 3: 'Strike'}, axis=1)

        
        def getNearStrike(PE_Data,premium):
            PE_Data['diff'] = abs(PE_Data.LTP - premium)
            PE_Data.sort_values(by = 'diff', inplace =True)
            return  PE_Data.iloc[0].to_dict()
        
        def getNearStrike(PE_Data,premium):
            PE_Data['diff'] = abs(PE_Data.LTP - premium)
            PE_Data.sort_values(by = 'diff', inplace =True)
            return  PE_Data.iloc[0].to_dict()

    dic = getNearStrike(PE_Data,float(PE_Primium))
    # Convert dictionary to DataFrame with a specified index
    df1 = pd.DataFrame([dic], index=['ID'])
    Symbol_PE = df1['Symbol'].iloc[0]
    Token_PE = df1['Token'].iloc[0]

    Text7.markdown(f"<u>Check Put-Strike Range</u>",unsafe_allow_html=True)
    Data1.write(df1)


    time.sleep(5)    
    Range  = int((StrikeRange)/25+1)
    infos = []
    ATM_Strike = atmStrike

    for i in range(Range):  
            Strike = ATM_Strike-StrikeRange
            #print(Strike)
            StrikeSymbol = f'{CommonSymbol}{Strike}CE'
            #print(StrikeSymbol)
            df = symbolDf[ (symbolDf['symbol'] == StrikeSymbol)]
            StrikeToken= df['token'].iloc[0]

            ltpInfo = Angel.obj.ltpData('NFO',StrikeSymbol,StrikeToken)
            
            Ltp = ltpInfo['data']['ltp']
            Token = ltpInfo['data']['symboltoken']
            Symbol = ltpInfo['data']['tradingsymbol']

            lst = [Symbol, Token,Ltp]  
            dframe = pd.DataFrame(lst) 
            df = dframe.T
            df=df.rename({0:'Symbol',1:'Token',2:'LTP'},axis=1)
            df['Strike'] = Strike
            infos.append(df)  
            ATM_Strike = ATM_Strike + 50
            
            CE_Data = pd.DataFrame(np.concatenate(infos))
            CE_Data = CE_Data.rename({0:'Symbol',1:'Token',2:'LTP',3:'Strike'},axis=1)
            #CE_Data        
            def getNearStrike(CE_Data,premium):
                CE_Data['diff'] = abs(CE_Data.LTP - premium)
                CE_Data.sort_values(by = 'diff', inplace =True)
                return  CE_Data.iloc[0].to_dict()

    dic1 = getNearStrike(CE_Data,float(CE_Primium))
    # Convert dictionary to DataFrame with a specified index
    df2 = pd.DataFrame([dic1], index=['ID'])
    Symbol_CE = df2['Symbol'].iloc[0]
    Token_CE = df2['Token'].iloc[0]

    Text8.markdown(f"<u>Check Call-Strike Range</u>",unsafe_allow_html=True)
    Data2.write(df2)


    Start_Date =datetime.datetime.now() - datetime.timedelta(days=3)
    End_Date = datetime.datetime.now()
    StockSymbol = "NSE:NIFTY50-INDEX"


    data = {"symbol": StockSymbol, "resolution": "5", "date_format": "1",
                "range_from": Start_Date.strftime('%Y-%m-%d'),
                "range_to": End_Date.strftime('%Y-%m-%d'), "cont_flag": "1"}

    historicaldata = Fyers.fyers.history(data)
    res_json = historicaldata
    try:
        hist_data = Fyers.fyers.history(data)
    except Exception as e:
        raise e
    df = pd.DataFrame(hist_data['candles'], columns=['date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Sh_MA'] = ta.sma(close=df['Close'], length=9)
    df['Lg_MA'] = ta.sma(close=df['Close'], length=26)
    df['RSI'] = ta.rsi(df.Close, length=14)
    #chart_placeholder.line_chart(df['Close'])

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df.index,y=df['Close'],name="LTP",yaxis='y1'))
    fig1.add_trace(go.Scatter(x=df.index,y=df['Sh_MA'],name="Sh_MA",yaxis='y1'))
    fig1.add_trace(go.Scatter(x=df.index,y=df['Lg_MA'],name="Lg_MA",yaxis='y1'))

    fig1.update_layout(autosize=False, width=1200, height=280, showlegend=True, margin={"l":0,"r":0,"t":0,"b":0})
    #st.subheader(f"{Optx_Symbol}-Chart Data Analysis")
    Chart.write(fig1)
    check_NSE_OPTX_Chain(Symbol_PE,Symbol_CE,Token_CE,Token_PE)


def check_NSE_OPTX_Chain(Symbol_PE,Symbol_CE,Token_CE,Token_PE):
    head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br"}

    URL1 = "https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY"

    NIFTY_URL = 'https://www.nseindia.com/api/quote-derivative?symbol=NIFTY'
    BNIFTY_URL = 'https://www.nseindia.com/api/quote-derivative?symbol=BANKNIFTY'

    symboldf = pd.read_csv('https://api.kite.trade/instruments')
    symboldf['expiry'] = pd.to_datetime(symboldf['expiry']).apply(lambda x: x.date())
    weekly_expiry = symboldf[(symboldf.segment == 'NFO-OPT')  &  (symboldf.name == 'NIFTY')]['expiry'].unique().tolist()
    weekly_expiry.sort()
    WEEKLY_EXPIRY = weekly_expiry[0]
    #WEEKLY_EXPIRY

    homeRes = requests.get(URL1, headers=head)
    d = requests.get(NIFTY_URL, headers=head, cookies=homeRes.cookies).json()
    df = pd.DataFrame(d['stocks'])
    timestamp = d['opt_timestamp']
    underling_value = d['underlyingValue']
    df1 = pd.json_normalize(df['metadata'])
    df1.insert(0, 'TimeStamp', timestamp)
    df1['TimeStamp']= pd.to_datetime(df1['TimeStamp'])
    df1['expiryDate']= pd.to_datetime(df1['expiryDate'])
    df1 = df1[['TimeStamp','expiryDate','lastPrice','pChange','numberOfContractsTraded','optionType','strikePrice']]
    df2 = pd.json_normalize(df['marketDeptOrderBook'])
    df2 = df2[[ 'tradeInfo.openInterest' ,'tradeInfo.changeinOpenInterest','otherInfo.impliedVolatility']]
    df2.fillna(0,inplace= True)

    final = pd.concat([df2, df1], axis='columns')

    #final = final[(final['tradeInfo.openInterest'] > 0) & (final['numberOfContractsTraded'] > 0)]
    final.columns = [c.strip() for c in final.columns.values.tolist()]
    final = final[final.expiryDate.dt.date ==WEEKLY_EXPIRY ]
    ceoc = final[final.optionType == 'Call']
    peoc =  final[final.optionType == 'Put']
    peoc = peoc.iloc[:, ::-1]
    finalOC = pd.merge(ceoc, peoc, how="outer", on=["strikePrice"])
    finalOC.sort_values(by = 'strikePrice',inplace =True)    
    
    StockSymbol = "NSE:NIFTY50-INDEX"
    data = {"symbol": StockSymbol, "ohlcv_flag": "1"}
    Msg = Fyers.fyers.depth(data)['d']
    df = pd.DataFrame(Msg)
    df = df.T
    LTP = df['ltp'].iloc[0]
    
    Atm_Strike = int(LTP/50)*50
    #Atm_Strike
    
    Upper_Range = Atm_Strike + 250
    Lower_Range = Atm_Strike - 250
    #Upper_Range
    #Lower_Range

    homeRes = requests.get(URL1, headers=head)
    d = requests.get(NIFTY_URL, headers=head, cookies=homeRes.cookies).json()
    df = pd.DataFrame(d['stocks'])
    timestamp = d['opt_timestamp']
    underling_value = d['underlyingValue']
    df1 = pd.json_normalize(df['metadata'])
    df1.insert(0, 'TimeStamp', timestamp)
    df1['TimeStamp']= pd.to_datetime(df1['TimeStamp'])
    df1['expiryDate']= pd.to_datetime(df1['expiryDate'])
    df1 = df1[['TimeStamp','expiryDate','lastPrice','pChange','numberOfContractsTraded','optionType','strikePrice']]
    df2 = pd.json_normalize(df['marketDeptOrderBook'])
    df2 = df2[[ 'tradeInfo.openInterest' ,'tradeInfo.changeinOpenInterest','otherInfo.impliedVolatility']]
    df2.fillna(0,inplace= True)

    final = pd.concat([df2, df1], axis='columns')

    #final = final[(final['tradeInfo.openInterest'] > 0) & (final['numberOfContractsTraded'] > 0)]
    final.columns = [c.strip() for c in final.columns.values.tolist()]
    final = final[final.expiryDate.dt.date ==WEEKLY_EXPIRY ]
    ceoc = final[final.optionType == 'Call']
    peoc =  final[final.optionType == 'Put']
    peoc = peoc.iloc[:, ::-1]
    finalOC = pd.merge(ceoc, peoc, how="outer", on=["strikePrice"])
    finalOC.sort_values(by = 'strikePrice',inplace =True)
    
    finalOC = finalOC[(finalOC['strikePrice'] >= Lower_Range) & (finalOC['strikePrice'] <= Upper_Range)]
    finalOC = finalOC[['tradeInfo.openInterest_x','tradeInfo.changeinOpenInterest_x','lastPrice_x','pChange_x','strikePrice','pChange_y','lastPrice_y','tradeInfo.changeinOpenInterest_y','tradeInfo.openInterest_y']]
    
    finalOC['Call-Prediction'] =""
    finalOC['Put-Prediction'] =""

    # CALL-SIDE CALCULATION
    for i in range(len(finalOC)):
        if finalOC['tradeInfo.changeinOpenInterest_x'].iloc[i]>0 and finalOC['pChange_x'].iloc[i]>0 :
            finalOC['Call-Prediction'].iloc[i] ="Fresh-Long"
            
        if finalOC['tradeInfo.changeinOpenInterest_x'].iloc[i]<0 and finalOC['pChange_x'].iloc[i]<0 :
            finalOC['Call-Prediction'].iloc[i] ="Long-Unwind"  
            
        if finalOC['tradeInfo.changeinOpenInterest_x'].iloc[i]>0 and finalOC['pChange_x'].iloc[i]<0 :
            finalOC['Call-Prediction'].iloc[i] ="Fresh-Short"
            
        if finalOC['tradeInfo.changeinOpenInterest_x'].iloc[i]<0 and finalOC['pChange_x'].iloc[i]>0 :
            finalOC['Call-Prediction'].iloc[i] ="Short-Covering"  
            

        if finalOC['tradeInfo.changeinOpenInterest_y'].iloc[i]>0 and finalOC['pChange_y'].iloc[i]>0 :
            finalOC['Put-Prediction'].iloc[i] ="Fresh-Long"
            
        if finalOC['tradeInfo.changeinOpenInterest_y'].iloc[i]<0 and finalOC['pChange_y'].iloc[i]<0 :
            finalOC['Put-Prediction'].iloc[i] ="Long-Unwind"  
            
        if finalOC['tradeInfo.changeinOpenInterest_y'].iloc[i]>0 and finalOC['pChange_y'].iloc[i]<0 :
            finalOC['Put-Prediction'].iloc[i] ="Fresh-Short"
            
        if finalOC['tradeInfo.changeinOpenInterest_y'].iloc[i]<0 and finalOC['pChange_y'].iloc[i]>0 :
            finalOC['Put-Prediction'].iloc[i] ="Short-Covering"         


    finalOC = finalOC[['Call-Prediction','tradeInfo.openInterest_x','tradeInfo.changeinOpenInterest_x','lastPrice_x','pChange_x','strikePrice','pChange_y','lastPrice_y','tradeInfo.changeinOpenInterest_y','tradeInfo.openInterest_y','Put-Prediction']]
    finalOC = round(finalOC,2)
    
    
    finalOC=finalOC.rename({'Call-Prediction':'Call-Prediction','tradeInfo.openInterest_x':'OI-Call','tradeInfo.changeinOpenInterest_x':'%-Chg OI-Call','lastPrice_x':'LTP-Call','pChange_x':'%Chg-LTP-Call','strikePrice':'strike_price','pChange_y':'%Chg-LTP-Put','lastPrice_y':'LTP-Put','tradeInfo.changeinOpenInterest_y':'%-Chg OI-Put','tradeInfo.openInterest_y':'OI-Put','Put-Prediction':'Put-Prediction'},axis=1)

    Data3.dataframe(finalOC)
    
    if timeNow > Common.TradeTime:
        # create a sample DataFrame
        df = finalOC['Call-Prediction'].iloc[5:9]        
        count = df.value_counts().get('Fresh-Short', 0)
        Text11.write(f"Call-Side Market Prediction = {count}")

        # create a sample DataFrame
        df = finalOC['Put-Prediction'].iloc[1:5]              
        count1 = df.value_counts().get('Fresh-Short', 0)  
        Text12.write(f"Put-Side Market Prediction = {count1}")

        position = Angel.obj.position()
        position = position['data']
        position = pd.DataFrame(position)
        position = position[(position['exchange'] == 'NFO') & (position['realised'] == 0)]
        len(position)

        if count == count1 == 4 and len(position)==0:
            Text14.write('Start Trading')

            # place order For CE Side
            try:
                orderparams = {
                    "variety": "NORMAL",
                    "tradingsymbol": Symbol_CE,
                    "symboltoken": Token_CE,
                    "transactiontype": "SELL",
                    "exchange": "NFO",
                    "ordertype": "MARKET",
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "price": "0",
                    "squareoff": "0",
                    "stoploss": "0",
                    "quantity": qty
                }
                orderId = Angel.obj.placeOrder(orderparams)
                st.write(f"The order is place for = {Symbol_CE} & id is: {orderId} & Trade Time is = {getTime()}")
            except Exception as e:
                st.write("Order placement failed: {}".format(e.message))  


            # place order For PE Side
            try:
                orderparams = {
                    "variety": "NORMAL",
                    "tradingsymbol": Symbol_PE,
                    "symboltoken": Token_PE,
                    "transactiontype": "SELL",
                    "exchange": "NFO",
                    "ordertype": "MARKET",
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "price": "0",
                    "squareoff": "0",
                    "stoploss": "0",
                    "quantity": qty
                }
                orderId = Angel.obj.placeOrder(orderparams)
                st.write(f"The order is place for = {Symbol_PE} & id is: {orderId} & Trade Time is = {getTime()}")
            except Exception as e:
                st.write("Order placement failed: {}".format(e.message)) 


        else :
                Text13.write(f'Wait for the Trading Moment = {getTime()}') 


    else:
        Hour1 = TradeTime // 60
        Min1 = TradeTime % 60
        Text10.write(f"Trade Will Be Started From {Hour1}:{Min1} AM, Present Time {getTime()}") 
           

def check_PL():
    position= Angel.obj.position()
    position =pd.DataFrame(position['data'])
    position = position[['symboltoken', 'tradingsymbol','symbolname', 'sellqty', 'realised', 'unrealised', 'pnl', 'sellavgprice','buyavgprice', 'ltp']]
    position = position.astype({'unrealised':'float','pnl':'float','ltp':'float','sellavgprice':'float','realised':'float','buyavgprice':'float'})
    position = position[ (position['symbolname'] == Optx_Symbol) & (position['realised'] == 0)]
    #position = position[ (position['symbolname'] =='BANKNIFTY')&(position['unrealised'] !='0.00')&(position['unrealised'] !='-0.00')]
    Data4.write(position)
    Unreleased_PNL = position['unrealised'].sum()
    Released_PNL = position['realised'].sum()
    Total_PNL = position['pnl'].sum()
   
    Text15.write(f"Total PNL = {Total_PNL}")
    Text16.write(f"Released PNL = {Released_PNL}")
    Text17.write(f"Unreleased PNL = {Unreleased_PNL}")

    for i in range(len(position)):
         if float(position['ltp'].iloc[i]) > 1.65*float(position['sellavgprice'].iloc[i]) :
             tradingsymbol = position['tradingsymbol'].iloc[i]
             symboltoken = position['token'].iloc[i]
             quantity = position['qty'].iloc[i]
             PNL = position['pnl'].iloc[i]

             st.write(f'Terminate {tradingsymbol}  for Loss of {PNL} ....!!')

             time.sleep(2)
             # place order
             try:
                 orderparams = {
                     "variety": "NORMAL",
                     "tradingsymbol": tradingsymbol,
                     "symboltoken": symboltoken,
                     "transactiontype": "BUY",
                     "exchange": "NFO",
                     "ordertype": "MARKET",
                     "producttype": "CARRYFORWARD",
                     "duration": "DAY",
                     "price": "0",
                     "squareoff": "0",
                     "stoploss": "0",
                     "quantity": quantity
                 }
                 orderId = Angel.obj.placeOrder(orderparams)
                 time.sleep(1)
                 st.write("The order id is: {}".format(orderId))
             except Exception as e:
                 st.write("Order placement failed: {}".format(e.message))



def main():
    global fyers
    timeNow = (datetime.datetime.now().hour*60 + datetime.datetime.now().minute)
    Hour = orderPlaceTime // 60
    Min = orderPlaceTime % 60

    while timeNow < Common.orderPlaceTime:
        text_placeholder = st.empty()
        st.write(f'Trade Will Be Started From {Hour}:{Min} AM, Present Time {getTime()} ')


    while timeNow < Common.orderPlaceTime:
        time.sleep(0.2)
        timeNow = (datetime.datetime.now().hour*60 + datetime.datetime.now().minute)
    print(f'Ready for Trading, Present Time {getTime()}/ Trade Close Time = {Common.closingTime//60}:{Common.closingTime%60} PM')


    while timeNow < Common.closingTime and timeNow > Common.orderPlaceTime:
        result = datetime.datetime.now().strftime("%I:%M:%S %p")        
        Text1.markdown(f"<u>Code will run after Every {interval} sec Interval , Current Time is-{result}</u>",unsafe_allow_html=True)
        #st.write('*****************************************************************************************************')
        #st.write(f"Code will run after {interval} sec                                  Current Time-{result}")
        #st.write('------------------------------------------------------------------------------------------------------')
        time.sleep(interval)
        check_PL()
        check_Common()
        #check_NSE_OPTX_Chain()



if __name__ == '__main__':
    main()

