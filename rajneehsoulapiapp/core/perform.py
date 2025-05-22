from datetime import datetime
from enum import Enum


from django.utils.timezone import now, is_naive, make_aware
from pytz import timezone

from rajneehsoulapiapp.core.weather_utils import send_weather_notification, create_pincode_weather_data_entry, \
    update_pincode_weather_data_entry, fetch_weather_data_by_pincode, get_user_mapped_entry, \
    get_pincode_weather_data_entry, get_weather_forecast_entry, get_pincode_weather_data_single_entry
from rajneehsoulapiapp.weather.models import WeatherPincodeMappedData

from rajneehsoulapiapp.core.weather_utils import (
    update_forecast_entry,
    create_forecast_entry,
)
from rajneehsoulapiapp.weather.models import WeatherForecast


def round_down_to_nearest_3hr(dt: datetime) -> datetime:
    """Rounds a datetime down to the nearest 3-hour interval."""
    dt_naive = dt.replace(tzinfo=None)
    rounded_hour = (dt_naive.hour // 3) * 3
    return dt_naive.replace(hour=rounded_hour, minute=0, second=0, microsecond=0)



from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Requires Python 3.9+
IST = ZoneInfo("Asia/Kolkata")

class TimeUnitType(Enum):
    Hour = 'hour'
    Minute = 'minute'
    Second = "second"

DIVISOR = 3600
def getTimeDelta(
        value: int,
        unit: TimeUnitType
) -> timedelta:
    if unit == TimeUnitType.Hour:
         return timedelta(hours=value)
    elif unit == TimeUnitType.Minute:
        return timedelta(minutes=value)
    else:
        return timedelta(seconds=value)
    # if unit == TimeUnitType.Hour:
    #     return timedelta(minutes=value)
    # else:
    #     return timedelta(minutes=value)

def get_adjusted_time(
    current_time: datetime,
    time_diff
) -> datetime | None:
    print(f"get_adjusted_time ~~~~~~~~~~~~~~~~> time-diff: ${time_diff}")

    if time_diff >= 3:
        td = current_time + getTimeDelta(3, TimeUnitType.Hour)
        return td
    elif time_diff >= 2:
        td = current_time + getTimeDelta(2, TimeUnitType.Hour)
        return td
    elif time_diff >= 1:
        td = current_time + getTimeDelta(1, TimeUnitType.Hour)
        return td
    else:
        return None

def get_adjusted_time_on_update(input_time: datetime, time_diff) -> datetime | None:
    print(f"get_adjusted_time_on_update -------------------> time-diff: ${time_diff}")

    if time_diff >= 3:
        td = input_time + getTimeDelta(3, TimeUnitType.Hour)
        return td
    elif time_diff >= 2:
        td = input_time + getTimeDelta(2, TimeUnitType.Hour)
        return td
    elif time_diff >= 1:
        td = input_time + getTimeDelta(1, TimeUnitType.Hour)
        return td
    else:
        return None

def get_time_until_update(
    time_diff
) -> str:
    print(f"get_time_until_update ~~~~~~~~~~~~~~~~~> time-diff: ${time_diff}")

    if time_diff >= 3:
        delay = getTimeDelta(3, TimeUnitType.Hour)
    elif time_diff >= 2:
        delay = getTimeDelta(2, TimeUnitType.Hour)
    elif time_diff >= 1:
        delay = getTimeDelta(1, TimeUnitType.Hour)
    else:
        return f"NOTIFY BLOCKED: ${"{:.2f}".format(time_diff)}"

    total_seconds = int(delay.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours} hr")
    if minutes > 0:
        parts.append(f"{minutes} min")
    if seconds > 0:
        parts.append(f"{seconds} sec")

    return " ".join(parts) if parts else "NA"


def get_time_until_update_on_update(time_diff) -> str:
    print(f"get_time_until_update_on_update -------------------------> time-diff: ${time_diff}")

    if time_diff >= 3:
        delay = getTimeDelta(3, TimeUnitType.Hour)
    elif time_diff >= 2:
        delay = getTimeDelta(2, TimeUnitType.Hour)
    elif time_diff >= 1:
        delay = getTimeDelta(1, TimeUnitType.Hour)
    else:
        return f"NOTIFY BLOCKED: {"{:.2f}".format(time_diff)}"


    total_seconds = int(delay.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours} hr")
    if minutes > 0:
        parts.append(f"{minutes} min")
    if seconds > 0:
        parts.append(f"{seconds} sec")

    return " ".join(parts) if parts else "NA"


def get_weather_forcast_data_for_pin_codes(pincodes) -> dict:
    weather_data_by_pincode = {}

    for pincode in pincodes:
        from rajneehsoulapiapp.core.weather_utils import fetch_weather_data_by_pincode
        raw_weather_data = fetch_weather_data_by_pincode(pincode)
        weather_data_by_pincode[pincode] = raw_weather_data

    return weather_data_by_pincode

def format_datetime_or_none(dt):
    if isinstance(dt, tuple):
        dt = dt[0]
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt is not None else None


def prepare_forcast_create_request(weather_data, notifyTime, notifyInTime) -> dict:
    weather_data["updated_count"] = 1
    weather_data["next_notify_in"] = notifyInTime
    weather_data["notify_count"] = 0
    weather_data["next_notify_at"] = format_datetime_or_none(notifyTime)
    from rajneehsoulapiapp.weather.models import NotifyMediumType
    weather_data["notify_medium"] = NotifyMediumType.EMAIL.value

    return weather_data


def prepare_forcast_update_request(
    current_time: datetime,
    existing_weather_forecast_data,
    nextNotifyAt: datetime,
    scheduledItem,
    isNotifyAccountable,
    time_diff = None
) -> dict:
    """
        Check last updated time is more than 1 min, Since scheduler is running in interval of 1 min.
        to avoid uncertain updates.
    """


    weather_data = {}

    """ Below check is to find next "notify date", 
                It should be less than or equal to (1 hr less than scheduled_date_time), 
                Since we stop notifying 1 hr before schedule_date_time
            """

    if isNotifyAccountable:
        getCalculatedNextNotifyTime = get_adjusted_time_on_update(
                nextNotifyAt,
                time_diff
            )
        weather_data.update({
            "updated_count": existing_weather_forecast_data.updated_count + 1,
            "notify_count": existing_weather_forecast_data.notify_count + 1,
            "next_notify_in": get_time_until_update_on_update(
                time_diff
            ),
            "next_notify_at": format_datetime_or_none(getCalculatedNextNotifyTime),
            "isWeatherNotifyEnabled": scheduledItem["isWeatherNotifyEnabled"]
        })
    else:
        weather_data.update({
            "updated_count": existing_weather_forecast_data.updated_count + 1,
            "isWeatherNotifyEnabled": scheduledItem["isWeatherNotifyEnabled"]
        })

    return weather_data

import json
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        # Handle datetime objects
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # Handle ScheduleItemList instances (convert them to dict)
        from rajneehsoulapiapp.schedule_list.models import ScheduleItemList
        if isinstance(obj, ScheduleItemList):
            return {
                "id": obj.id,
                "user_id": obj.user.id if obj.user else None,
                "google_auth_user_id": obj.google_auth_user.id if obj.google_auth_user else None,
                "dateTime": obj.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
                "title": obj.title,
                "isItemPinned": obj.isItemPinned,
                "lastScheduleOn": obj.lastScheduleOn,
                "subTitle": obj.subTitle,
                "isArchived": obj.isArchived,
                "priority": obj.priority,
                "isWeatherNotifyEnabled": obj.isWeatherNotifyEnabled,
            }
        # Fallback to default behavior for other objects
        return super().default(obj)



def trigger_task():
    """
    Fetches weather forecast for upcoming schedule items within 24 hours,
    updates or creates forecast entries, and computes notification metadata.
    """

    print("\n➡️ - - - EXECUTION STARTED - - - ➡️")

    get_user_mapped_data = get_user_mapped_entry()

    # Extract user_info
    user_info = get_user_mapped_data["user_info"]

    pincodes = get_user_mapped_data["pincodes"]

    ist = timezone("Asia/Kolkata")
    current_time = now()

    if is_naive(current_time):
        current_time = make_aware(current_time, timezone=ist)
    else:
        current_time = current_time.astimezone(ist)

    for pincode in pincodes:
        pincode_weather_data = get_pincode_weather_data_single_entry(pincode)

        if pincode_weather_data:
            # print(f"weather-pinned-data: {pincode_weather_data}")
            print(f"pincode_weather_data updated_count: {pincode_weather_data["updated_count"]}")
            print(f"pincode_weather_data: last_updated: {pincode_weather_data["last_updated"]}")
            last_updated_count = pincode_weather_data["updated_count"]
            last_updated_stored_weather_pin_data = datetime.fromisoformat(pincode_weather_data["last_updated"])
            if last_updated_stored_weather_pin_data.tzinfo is None:
                last_updated_stored_weather_pin_data = make_aware(last_updated_stored_weather_pin_data)

            getLastUpdatedWeatherPinData = last_updated_stored_weather_pin_data.astimezone(ist)

            time_diff = abs((getLastUpdatedWeatherPinData - current_time).total_seconds()) / DIVISOR
            print(f"time diff ---------------{pincode} ---- time_diff > 3.00 ------------------------> {time_diff}")

            if time_diff > 3.00:
                weather_forecast_data = get_weather_forcast_data_for_pin_codes([pincode])
                update_pincode_weather_data_entry(weather_forecast_data, last_updated_count)
            else:
                print(f"SKIP weather_forcast_data saved data updation, Time Diff :  {time_diff}")

        else:  # post-entry for all pincode data
            print("No data exists, Calling weather api !")
            if pincode:
                weather_api_data = get_weather_forcast_data_for_pin_codes([pincode])
                create_pincode_weather_data_entry(weather_api_data)
            else:
                print("NO WEATHER FORECAST EXPIRED DATA FOUND !")

    # Extract all address and schedule_item entries
    bulk_data = get_user_mapped_data["bulk_data"]

    for entry in bulk_data:
        email_id = user_info["emailId"]
        address = entry["address"]
        schedule_items = entry["schedule_item"]

        pincode = address["pincode"]
        schedule_items_title = schedule_items["title"]
        schedule_items_date_time = schedule_items["dateTime"]
        schedule_items_isWeatherNotifyEnabled = schedule_items["isWeatherNotifyEnabled"]


        """ This if condition states that, When scheduled_date_time is in b/w current_date_time
            and current_date_time + 24 hrs (i.e 24 hrs from current_date_time)
        """
        schedule_items_date_time = ist.localize(datetime.strptime(schedule_items_date_time, "%Y-%m-%d %H:%M"))

        if not (current_time <= schedule_items_date_time <= current_time + timedelta(hours=24)):
            """
                This block simple states that scheduled_date_time is expired, or
                it not scheduled within next day (current_Date_time + 24hrs).
            """
            from rajneehsoulapiapp.schedule_list.models import ScheduleItemList

            # Step 1: Retrieve expired schedule items
            expired_schedule_items = ScheduleItemList.objects.filter(
                dateTime__lt=current_time
            )

            # Step 2: Update related forecasts if expired schedule items exist
            if expired_schedule_items.exists():
                # Using the ForeignKey relationship to fetch forecasts related to expired schedule items
                forecasts_to_update = WeatherForecast.objects.filter(
                    scheduleItem__in=expired_schedule_items,  # Using the related field in ForeignKey
                    isActive=True,
                )

                if forecasts_to_update.exists():
                    updated_count = forecasts_to_update.update(
                        isActive=False,
                        # Assuming the WeatherForecast model has a field like 'last_updated'
                        last_updated=now()  # Example field if you have it
                    )
                    print(f"✅ Updated {updated_count} expired forecast(s).")
                else:
                    print("✅ forecasts found is expired ")
            else:
                print("✅ schedule items found is expired ")


        else:
            """
                This block simple states that scheduled_date_time lies within next day (current_Date_time + 24hrs).
            """

            """ Logic to find weather data for scheduled_date_time from fetched Weather api data """
            pinned_weather_forecast_list = pincode_weather_data.get("weather_data").get("list", [])
            rounded_schedule = round_down_to_nearest_3hr(schedule_items_date_time)
            revisedScheduleDateTime = schedule_items_date_time - getTimeDelta(1, TimeUnitType.Hour)

            matched_forecast = None
            for entry in pinned_weather_forecast_list:
                try:
                    entry_time = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    if entry_time == rounded_schedule:
                        matched_forecast = entry
                        break
                except Exception as e:
                    print("⛔ Error parsing fore cast entry:", e)

            """ Below code start to create request body params data to create/update Weather Forecast Data."""

            unique_key = f"{pincode}-{schedule_items["id"]}"

            forecast_time_dt = datetime.strptime(matched_forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
            forecast_time_ist = timezone("Asia/Kolkata").localize(forecast_time_dt)
            forecast_time_str = forecast_time_ist.strftime("%Y-%m-%dT%H:%M:%S")

            existing_weather_forecast_data: WeatherForecast = WeatherForecast.objects.filter(
                unique_key=unique_key,
                pincode=pincode,
                forecast_time=forecast_time_ist,
            ).first()

            if existing_weather_forecast_data:
                nextNotifyAt = existing_weather_forecast_data.next_notify_at

                if nextNotifyAt is not None:
                    # Convert the date and time into IST
                    # Make schedule_time timezone-aware
                    if is_naive(nextNotifyAt):
                        nextNotifyAt = make_aware(nextNotifyAt, timezone=IST)
                    else:
                        nextNotifyAt = nextNotifyAt.astimezone(IST)

                    isTimeToSendEmailWithUpdate = nextNotifyAt < current_time
                    print(
                        f"💡 isTimeToSendEmailWithUpdate: {isTimeToSendEmailWithUpdate} | Time left : {abs(nextNotifyAt - current_time)}")

                    print(f"🟣 nextNotifyAt : {nextNotifyAt} | current_time : {current_time}")
                    print(f"🔵 nextNotifyAt : {nextNotifyAt} | revisedScheduleDateTime : {revisedScheduleDateTime}")

                    if isTimeToSendEmailWithUpdate:
                        print(
                            f"abs(nextNotifyAt - revisedScheduleDateTime).total_seconds() : {abs(nextNotifyAt - revisedScheduleDateTime).total_seconds()}")
                        print(
                            f"abs(nextNotifyAt - revisedScheduleDateTime).total_seconds() / 60 (Mins LEFT) : {abs(nextNotifyAt - revisedScheduleDateTime).total_seconds() / 60}")
                        print(
                            f"💡 abs(nextNotifyAt - revisedScheduleDateTime).total_seconds() / 3600 (Hours LEFT) : {abs(nextNotifyAt - revisedScheduleDateTime).total_seconds() / 3600}")
                        time_diff = int(abs(nextNotifyAt - revisedScheduleDateTime).total_seconds() / DIVISOR)
                        print(
                            f"time_diff to calculate next nextNotifyAt variable value by comparing to revisedScheduleDateTime : {time_diff}")

                        update_request = prepare_forcast_update_request(
                            current_time=current_time,
                            existing_weather_forecast_data=existing_weather_forecast_data,
                            nextNotifyAt=nextNotifyAt,
                            scheduledItem=schedule_items,
                            time_diff=time_diff,
                            isNotifyAccountable=True
                        )
                        update_forecast_entry(
                            existing_weather_forecast_data.id,
                            forecast_data=update_request
                        )
                        print("Proceed to send email =>")
                        emailRequestBody = {
                            "emailId": email_id,
                            "task_name": schedule_items["title"],
                            "schedule_date_time": schedule_items_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                            "weather_status": f"{existing_weather_forecast_data.weatherType}, {existing_weather_forecast_data.weatherDescription}"
                        }
                        send_weather_notification(
                            request=emailRequestBody
                        )
                    else:
                        print(f"UPDATE update_forecast_entry: isNotifyAccountable : false")
                        update_request = prepare_forcast_update_request(
                            current_time=current_time,
                            existing_weather_forecast_data=existing_weather_forecast_data,
                            nextNotifyAt=nextNotifyAt,
                            scheduledItem=schedule_items,
                            isNotifyAccountable=False
                        )
                        update_forecast_entry(
                            existing_weather_forecast_data.id,
                            forecast_data=update_request
                        )

                else:
                    print("🔴 Next_notify_at is None. 🔴")


            else:
                weather_data = {
                    "pincode": pincode,
                    "unique_key": unique_key,
                    "forecast_time": forecast_time_str,
                    "timeStamp": matched_forecast["dt"],
                    "weatherType": matched_forecast["weather"][0]["main"],
                    "weatherDescription": matched_forecast["weather"][0]["description"],
                    "temperature_celsius": matched_forecast["main"]["temp"],
                    "humidity_percent": matched_forecast["main"]["humidity"],
                    "scheduleItem": json.dumps(schedule_items, cls=CustomJSONEncoder)
                }


                print(f"WHILE CREATE : revisedScheduleDateTime -> {revisedScheduleDateTime}")
                print(f"WHILE CREATE : current_time -> {current_time}")

                time_diff = abs((revisedScheduleDateTime - current_time).total_seconds()) / DIVISOR
                print(f"WHILE CREATE : time_diff of abs((revisedScheduleDateTime - current_time) -> {time_diff}")
                time_diff = round(time_diff)
                print(f"WHILE CREATE : round off time_diff of abs((revisedScheduleDateTime - current_time) -> {time_diff}")

                assumed_notify_time = get_adjusted_time(current_time, time_diff)
                print(f"assumed_notify_time : {assumed_notify_time}")

                if assumed_notify_time > revisedScheduleDateTime:
                    print(f"assumed_notify_time : {assumed_notify_time} is GREATER THAN revisedScheduleDateTime : {revisedScheduleDateTime}")
                    notifyTime = revisedScheduleDateTime - timedelta(minutes=5)
                    print(f"notify time will be less than 5 min before current time i.e {notifyTime}")
                    time_diff_for_notifyIn = abs(notifyTime - current_time).total_seconds() / DIVISOR

                else:
                    print(f"notify time will be assumed_notify_time: {assumed_notify_time}")
                    notifyTime = assumed_notify_time
                    time_diff_for_notifyIn = time_diff

                print(f"time_diff_for_notifyIn : {time_diff_for_notifyIn}")
                time_diff_for_notifyIn = round(time_diff_for_notifyIn)
                print(f"time_diff_for_notifyIn round : {time_diff_for_notifyIn}")

                create_forecast_entry(
                    forecast_data=prepare_forcast_create_request(
                        weather_data=weather_data,
                        notifyTime = notifyTime,
                        notifyInTime =  get_time_until_update(time_diff_for_notifyIn)
                    )
                )

    print("\n🔚 - - - EXECUTION OVER - - - 🔚")

