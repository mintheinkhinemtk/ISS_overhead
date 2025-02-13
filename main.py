import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 1.326253 # Your latitude
MY_LONG = 103.856757 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
def iss_overhead(iss_lat,iss_lng):
    if (MY_LAT-5 <= iss_lat <= MY_LAT+5) and (MY_LONG-5 <= iss_lng <= MY_LONG+5):
        return True
    else:
        return False


def is_dark(): # is the sky dark or not
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    resp = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    resp.raise_for_status()
    data = resp.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False

while True:
    time.sleep(60) # run every 60 secs
    if iss_overhead(iss_latitude,iss_longitude) and is_dark():
        connection = smtplib.SMTP("smtp.gmail.com") # for sending mail
        my_email = "abc@gmail.com" # your email
        my_pass = "abc" # your password
        connection.starttls()
        connection.login(my_email,my_pass)
        connection.sendmail(
            from_addr=my_email,
            to_addrs = my_email,
            msg="Subject:Look Up \n\n The ISS is above you in the sky."
        )






