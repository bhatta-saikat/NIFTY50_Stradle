from SmartApi import SmartConnect, SmartWebSocket
import pyotp
import pandas as pd

from datetime import datetime
import time
import requests
import pandas as pd
import pyotp
import pytz

from SmartApi import SmartConnect

api_key='C46AImmE'
ClientID='M507690'
Password='4663'


#create object of call
obj=SmartConnect(api_key=api_key)

data = obj.generateSession(ClientID,Password,pyotp.TOTP("4ACNNSIZL6EV6UQ2ACSI23H5VQ").now())
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
userProfile= obj.getProfile(refreshToken)
User= pd.DataFrame(userProfile)
User = User['data']['name']
User

print(f"Welcome {User} to the World of SMART API BY ANGEL.....!!")
print(f"Login Sucessfull....!!")