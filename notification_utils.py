from datetime import datetime, timedelta

def parse_duration(duration):
    """
    Parse a flexible duration string into a timedelta object.

    Args:
        duration (str): Duration string (e.g., '30 min', '1 day', '2 hours').

    Returns:
        timedelta: Corresponding timedelta object.
    """
    parts = duration.split()
    if len(parts) != 2:
        raise ValueError("Invalid duration format. Use '<number> <unit>' (e.g., '30 min', '1 day').")

    value, unit = int(parts[0]), parts[1].lower()
    if unit in ['min', 'minute', 'minutes']:
        return timedelta(minutes=value)
    elif unit in ['hour', 'hours']:
        return timedelta(hours=value)
    elif unit in ['day', 'days']:
        return timedelta(days=value)
    elif unit in ['week', 'weeks']:
        return timedelta(weeks=value)
    else:
        raise ValueError("Unsupported time unit. Use 'min', 'hours', 'days', or 'weeks'.")

def check_date_difference(weather_date_time, given, allowed_duration):
    # Convert string inputs to datetime objects
    current_dt = datetime.strptime(weather_date_time, '%Y-%m-%d %H:%M:%S')
    given_dt = datetime.strptime(given, '%Y-%m-%d %H:%M:%S')


    # print("current_dt : ", current_dt)
    # print("given_dt : ", given_dt)

    difference = abs(given_dt - current_dt)

    #print("-"*20)

    # Parse allowed_duration
    max_duration = parse_duration(allowed_duration)

    # Check if the given date is within the allowed duration
    return weather_date_time < given and difference <= max_duration


from datetime import datetime


def find_datetime_range(data_list, given_datetime):
    """
    Finds the range in which the given datetime falls.

    :param data_list: List of dictionaries with datetime and weather info
    :param given_datetime: The datetime to check (string format: 'YYYY-MM-DD HH:MM:SS')
    :return: A dictionary with start, end range, and weather description or None if not found
    """
    given_dt = datetime.strptime(given_datetime, "%Y-%m-%d %H:%M:%S")

    for i in range(len(data_list) - 1):
        start_dt = datetime.strptime(data_list[i]['dt_txt'], "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(data_list[i + 1]['dt_txt'], "%Y-%m-%d %H:%M:%S")

        # Check if the given datetime falls within this range
        if start_dt <= given_dt < end_dt:
            return {
                "start_range": data_list[i]['dt_txt'],
                "end_range": data_list[i + 1]['dt_txt'],
                "weather_info": data_list[i]["weather"][0]["description"]
            }

    return None  # If no range matches


from datetime import datetime


def format_date(date_str):
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d ")

    # Format the date into the desired format
    formatted_date = date_obj.strftime("%d %b, %y")

    # Add the ordinal suffix (st, nd, rd, th)
    day = int(date_obj.strftime("%d"))
    suffix = 'th'
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    formatted_date = formatted_date.replace(f"{day:02}", f"{day}{suffix}")

    return formatted_date