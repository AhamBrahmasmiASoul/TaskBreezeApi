import requests
from firebase_admin import *

from notification_utils import check_date_difference, find_datetime_range
from rajneehsoulapiapp.communication.mail import send_email_anonymous

api_address = "https://api.openweathermap.org/data/2.5/forecast?appid=61d38a3c289f168e130b1fa745c9a37c&q="

url = api_address + "Gurugram"

json_data = requests.get(url).json()
json_string = json.dumps(json_data, indent=4)
data = json.loads(json_string)
allowedList = []
for i in range(len(data['list'])):
    weather_date_time = data['list'][i]['dt_txt']

    allowed_diff = check_date_difference(weather_date_time, "2025-01-18 12:00:00", "1 Day")
    if allowed_diff:
        weathers_date_time = weather_date_time.split(" ")
        weathers_date = weathers_date_time[0]
        wsd = weathers_date.split("-")
        wsd_only_date = wsd[2]
        print("info: ", weather_date_time)
        allowedList.append(data['list'][i])
        print("weather info : ", data['list'][i]["weather"][0]["description"])

print("allowedList: ", allowedList)
result = find_datetime_range(allowedList, "2025-01-19 00:00:00")



send_email_anonymous("rajneeshkrsharma98@gmail.com", result["start_range"], result["weather_info"])


