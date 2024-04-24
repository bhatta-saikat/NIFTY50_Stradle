from breeze_connect import BreezeConnect
import datetime
import pandas as pd

your_api_key ='600V9$52664(5u8*29L88M5Z0)5G0qk9'
your_secret_key = '993314i8330q08r^1m6Y29539o3985#8'
your_api_session='39400898'

# Initialize SDK
# Initialize SDK
breeze = BreezeConnect(api_key=your_api_key)



# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
import urllib
print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(your_api_key))

# Generate Session
breeze.generate_session(api_secret=your_secret_key,session_token=your_api_session)

# Generate ISO8601 Date/DateTime String
import datetime
iso_date_string = datetime.datetime.strptime("28/02/2021","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
iso_date_time_string = datetime.datetime.strptime("28/02/2021 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'

print("Welcome To ICICI_DIRECT Algo wrld.....!!")