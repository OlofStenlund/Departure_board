import python_jwt as jwt
import requests
import pandas as pd
from datetime import datetime, time, timedelta
import time
from personal_info import token_generation_base_url, token_generation_headers, connection_base_url, connection_url


stop = "Brunnsbotorget"

# Setup-functions
def save_token(token):
    with open("token.txt", "w") as file:
        file.write(token)

def read_token():
    with open("token.txt", "r") as file:
        token = file.read().strip()
        return token 

def get_token_expiry(token):
    token = token
    decoded_token = jwt.process_jwt(token)
    expiry = decoded_token[1]['exp']-3
    start = datetime(1970, 1, 1)
    exp = start + timedelta(0,expiry)
    return exp, token

def generate_token():
    resp = requests.post(token_generation_base_url, data='grant_type=client_credentials', headers = token_generation_headers)
    data = resp.json()
    token = data['access_token']
    return token


# These functions need variables established above
def get_gid(base_url, url, headers):
    resp = requests.get(f"{base_url}{url}", headers=headers)
    data = resp.json()
    gid = data['results'][0]['gid']
    return gid

def convert_str_to_datetime(departures_data, i):
    dep_year = pd.to_numeric(departures_data['results'][i]['estimatedOtherwisePlannedTime'][:4])
    dep_year
    dep_month = pd.to_numeric(departures_data['results'][i]['estimatedOtherwisePlannedTime'][5:7])
    dep_month
    dep_day = pd.to_numeric(departures_data['results'][i]['estimatedOtherwisePlannedTime'][8:10])
    dep_day
    dep_hour = pd.to_numeric(departures_data['results'][i]['estimatedOtherwisePlannedTime'][11:13])
    dep_hour
    dep_minute = pd.to_numeric(departures_data['results'][i]['estimatedOtherwisePlannedTime'][14:16])
    dep_minute
    return datetime(year=dep_year, month=dep_month, day=dep_day, hour=dep_hour, minute=dep_minute, second=1, microsecond=1)

def get_departures_list(departures_data, now):
    departures_list = []
    for i, data in enumerate(departures_data['results']):
        bus_number = departures_data['results'][i]['serviceJourney']['line']['shortName']
        bus_direction = departures_data['results'][i]['serviceJourney']['direction']
        estimated_departure = departures_data['results'][i]['estimatedOtherwisePlannedTime'][11:16]
        planned_departure = departures_data['results'][i]['plannedTime'][11:16]
        platform = departures_data['results'][i]['stopPoint']['platform']
        est_departure_time_obj = convert_str_to_datetime(departures_data, i)
        leaves_in = est_departure_time_obj - now
        leaves_in_sec = leaves_in.total_seconds()
        leaves_in_minutes = divmod(leaves_in_sec, 60)[0]
        leaves_in_minutes = int(leaves_in_minutes)
        if leaves_in_minutes >= 0:
            if leaves_in_minutes == 0:
                leaves_in_minutes = "Nu"
            else: 
                pass
            departures_list.append({"bus_number": {bus_number}, "bus_direction": {bus_direction}, "platform": {platform}, "planned_departure": {planned_departure}, "estimated_departure": {estimated_departure}, "time_until_dearture": {leaves_in_minutes}})
    return departures_list

def get_current_times(now):
    current_year, current_week = now.isocalendar()[0], now.isocalendar()[1]
    current_month = now.month
    current_day = now.day
    current_hour = now.hour
    if current_hour < 10:
        current_hour = str(current_hour)
        current_hour = f"0{current_hour}"
    current_minute = now.minute
    if current_minute < 10:
        current_minute = str(current_minute)
        current_minute = f"0{current_minute}"
    current_day_name = now.strftime("%A")
    current_month_name = now.strftime("%B")
    return [current_year, current_month, current_month_name, current_week, current_day, current_day_name, current_hour, current_minute] 


def main():
    # Get token expiry
    now = datetime.now()
    token = read_token()
    token_expiry, token = get_token_expiry(token)
    valid_time = token_expiry - now
    valid_seconds = valid_time.total_seconds()
        

    if valid_seconds <= 3:
        print("New token needed. Stand by...")
        time.sleep(4)
        token = generate_token()
        save_token(token)
    elif valid_seconds > 3:
        pass
    else: 
        ValueError
    
    # Adapt script to token
    bearer_token = f'Bearer {token}'
    connection_headers = {f'Authorization': bearer_token}
    
    gid = get_gid(connection_base_url, connection_url, connection_headers)
    get_departures_url = f"/stop-areas/{gid}/departures?limit=10"
    departures_response = requests.get(f"{connection_base_url}{get_departures_url}", headers=connection_headers)
    departures_data = departures_response.json()
    departures = get_departures_list(departures_data, now)
    current_time = get_current_times(now)
    return departures, current_time