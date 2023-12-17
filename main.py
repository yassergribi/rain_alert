import requests
import os
from twilio.rest import Client


twilio_phone = os.environ["TWILIO_PHONE"]
my_phone = os.environ["MY_PHONE"]

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

OWM_URL = "https://api.openweathermap.org/data/3.0/onecall"
MY_LAT = 54.335361
MY_LONG = -7.624020
api_key = os.environ['API_KEY']


params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid":api_key,
    "exclude":"current,minutely,daily"
}


response = requests.get(url=OWM_URL, params=params)
# print(response)
response.raise_for_status()
weather_data = response.json()

weather_slice = weather_data["hourly"][:12]


will_rain = False
for hour_data in weather_slice:
    if hour_data["weather"][0]["id"] < 700:
        will_rain = True
        break

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body="Its going to rain today, Remember to bring an ☂️",
                     from_= twilio_phone,
                     to= my_phone
                 )

    print(message.status)