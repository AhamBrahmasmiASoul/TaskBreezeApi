import httpx

from rajneeshsoulapi.settings import OPEN_WEATHER_MAP_API_KEY


def fetch_weather_data_by_pincode(pincode):
    url = f"https://api.openweathermap.org/data/2.5/forecast?zip={pincode},IN&appid={OPEN_WEATHER_MAP_API_KEY}"
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Failed to fetch weather for pincode {pincode}. Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None

def get_weather_forecast_entry():
    url = "http://localhost:8000/api/weather/forecast?expired=false"
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            print("✅ get_weather_forecast_entry successfully!")
            return response.json()
        else:
            print(f"get_weather_forecast_entry Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None

def create_forecast_entry(forecast_data):
    url = "http://localhost:8000/api/weather/forecast"
    print(f"Request create for forecast_data: {forecast_data}")
    try:
        response = httpx.post(url, json=forecast_data)
        if response.status_code == 201:
            print("✅ Forecast data created successfully!")
            return response.json()
        else:
            print(f"⚠️ Failed to create forecast. Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None


def update_forecast_entry(forecast_id, forecast_data):
    url = f"http://localhost:8000/api/weather/forecast?forecast_id={forecast_id}"
    print(f"request data for forecast_data update : {forecast_data}")
    try:
        response = httpx.patch(url, json=forecast_data)
        if response.status_code == 200:
            print(f"✅ Forecast data with ID {forecast_id} updated successfully!")
            return response.json()
        else:
            print(f"⚠️ Failed to update forecast with ID {forecast_id}. Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None


def send_weather_notification(request):
    url = "http://localhost:8000/api/communication/send-weather-notify-email"
    #print(f"request: {request}")
    try:
        response = httpx.post(url, json=request)
        if response.status_code == 200:
            print("✅ Email sent successfully!")
            return response.json()
        else:
            print(f"⚠️ Failed to send email. Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None


def create_pincode_weather_data_entry(pincode_weather_data):
    pincode, weather_data = next(iter(pincode_weather_data.items()))
    requestBody = {
        "pincode": pincode,
        "weather_data": weather_data,
        "updated_count": 0
    }

    #print(f"requestBody: {requestBody}")

    url = "http://localhost:8000/api/weather/pincode-weather-mapping"
    try:
        response = httpx.post(url, json=requestBody)
        if response.status_code == 201:
            print("✅ pincode_weather_data created successfully!")
            return response.json()
        else:
            print(f"⚠️ Failed to create pincode_weather_data. Status: {response.status_code}")
            try:
                print("Error Response:", response.json())
            except Exception:
                print("Error Response:", response.text)
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None


def update_pincode_weather_data_entry(pincode_weather_data, last_updated_count):
    #print(f"pincode_weather_data: {pincode_weather_data}")
    try:
        for key, value in pincode_weather_data.items():
            request = {
                "weather_data" : value,
                "updated_count" : last_updated_count + 1
            }

            url = f"http://localhost:8000/api/weather/pincode-weather-mapping?pincode={key}"
            response = httpx.patch(url, json=request)

            if response.status_code == 200:
                print(f"✅ pincode_weather_data for {key} updated successfully!")
                return response.json()
            else:
                print(f"⚠️ Failed to update pincode_weather_data for {key}. Status: {response.status_code}")
                return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None

def get_pincode_weather_data_entry():
    try:
        url = f"http://localhost:8000/api/weather/pincode-weather-mapping"
        response = httpx.get(url)

        if response.status_code == 200:
            print(f"✅  get_pincode_weather_data_entry successfully!")
            return response.json()
        else:
            print(f"⚠️ Failed to get_pincode_weather_data_entry. Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None

def get_pincode_weather_data_single_entry(key):
    try:
        url = f"http://localhost:8000/api/weather/pincode-weather-mapping?pincode={key}"
        response = httpx.get(url)

        if response.status_code == 200:
            print(f"✅  get_pincode_weather_data_entry successfully!")
            return response.json()
        else:
            print(f"⚠️ Failed to get_pincode_weather_data_entry. Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None

def get_user_mapped_entry():
    try:
        url = f"http://localhost:8000/api/weather/get-user-mapping"
        response = httpx.get(url)

        if response.status_code == 200:
            print(f"✅  get_user_mapped_entry successfully!")
            return response.json()
        else:
            print(f"⚠️ Failed to get_user_mapped_entry. Status: {response.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"❌ Request error: {e}")
        return None
