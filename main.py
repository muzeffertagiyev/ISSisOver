import requests
import datetime as dt
import smtplib
import time
import os

# MY_LAT = 40.593849
# MY_LNG = 49.665161
MY_EMAIL = os.environ['EMAIL']
EMAIL_PASSWORD = os.environ['PASSWORD']

MY_LAT = -51.3646
MY_LNG = 12.6989


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


if is_iss_overhead() and is_night():
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs='t.muzeffer@yahoo.com', msg='Subject:ISS\n\n Look Up')
        print('Email was sent successfully')
