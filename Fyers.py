import json
import requests
import time
import pyotp
import os
import requests
from urllib.parse import parse_qs,urlparse
import sys
from fyers_api import fyersModel
from fyers_api import accessToken

from datetime import datetime, timedelta
import datetime


from datetime import datetime, timedelta, date
from time import sleep
import os
import pyotp
import requests
import json
import math
import pytz
from urllib.parse import parse_qs, urlparse
import warnings
import pandas as pd

pd.set_option('display.max_columns', None)
warnings.filterwarnings('ignore')

import base64

APP_ID =  "JKRFLKWBAI" # App ID from myapi dashboard is in the form appId-appType. Example - EGNI8CE27Q-100, In this code EGNI8CE27Q will be APP_ID and 100 will be the APP_TYPE
APP_TYPE = "100"
SECRET_KEY = 'IMOJFE3DVX'
client_id= f'{APP_ID}-{APP_TYPE}'

FY_ID = "XM11096"  # Your fyers ID
APP_ID_TYPE = "2"  # Keep default as 2, It denotes web login
TOTP_KEY = "KN4BIMFJARM4YCX6UVHUI6FGKP4MUIXZ"  # TOTP secret is generated when we enable 2Factor TOTP from myaccount portal
PIN = "4663"  # User pin for fyers account

redirect_uri = "http://127.0.0.1:5000/login"
client_id='JKRFLKWBAI-100'
secret_key = 'IMOJFE3DVX'
FY_ID = "XM11096"  # Your fyers ID
TOTP_KEY = "KN4BIMFJARM4YCX6UVHUI6FGKP4MUIXZ"  # TOTP secret is generated when we enable 2Factor TOTP from myaccount portal
PIN = "4663"  # User pin for fyers account

from fyers_apiv3 import fyersModel


"""
In order to get started with Fyers API we would like you to do the following things first.
1. Checkout our API docs :   https://myapi.fyers.in/docsv3
2. Create an APP using our API dashboard :   https://myapi.fyers.in/dashboard/

Once you have created an APP you can start using the below SDK 
"""

#### Generate an authcode and then make a request to generate an accessToken (Login Flow)

                         ## app_secret key which you got after creating the app
grant_type = "authorization_code"                  ## The grant_type always has to be "authorization_code"
response_type = "code"                             ## The response_type always has to be "code"
state = "sample"                                   ##  The state field here acts as a session manager. you will be sent with the state field after successfull generation of auth_code


### Connect to the sessionModel object here with the required input parameters
appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)

# ## Make  a request to generate_authcode object this will return a login url which you need to open in your browser from where you can get the generated auth_code
generateTokenUrl = appSession.generate_authcode()
generateTokenUrl



def getEncodedString(string):
    string = str(string)
    base64_bytes = base64.b64encode(string.encode("ascii"))
    return base64_bytes.decode("ascii")


URL_SEND_LOGIN_OTP = "https://api-t2.fyers.in/vagator/v2/send_login_otp_v2"
res = requests.post(url=URL_SEND_LOGIN_OTP, json={"fy_id": getEncodedString(FY_ID), "app_id": "2"}).json()
print(res)

if datetime.now().second % 30 > 27: sleep(5)
URL_VERIFY_OTP = "https://api-t2.fyers.in/vagator/v2/verify_otp"
res2 = requests.post(url=URL_VERIFY_OTP,
                     json={"request_key": res["request_key"], "otp": pyotp.TOTP(TOTP_KEY).now()}).json()
print(res2)

ses = requests.Session()
URL_VERIFY_OTP2 = "https://api-t2.fyers.in/vagator/v2/verify_pin_v2"
payload2 = {"request_key": res2["request_key"], "identity_type": "pin", "identifier": getEncodedString(PIN)}
res3 = ses.post(url=URL_VERIFY_OTP2, json=payload2).json()
print(res3)

ses.headers.update({
    'authorization': f"Bearer {res3['data']['access_token']}"
})

TOKENURL = "https://api-t1.fyers.in/api/v3/token"
payload3 = {"fyers_id": FY_ID,
            "app_id": client_id[:-4],
            "redirect_uri": redirect_uri,
            "appType": "100", "code_challenge": "",
            "state": "None", "scope": "", "nonce": "", "response_type": "code", "create_cookie": True}

res3 = ses.post(url=TOKENURL, json=payload3).json()
print(res3)

url = res3['Url']
print(url)
parsed = urlparse(url)
auth_code = parse_qs(parsed.query)['auth_code'][0]
auth_code

grant_type = "authorization_code"

response_type = "code"

session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
)

session.set_token(auth_code)
response = session.generate_token()
access_token = response['access_token']

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path=os.getcwd())

#fyers.get_profile()
print('Welcome To Fyers Algo World........')