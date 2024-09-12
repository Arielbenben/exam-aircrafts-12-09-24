import requests
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from functools import partial
from toolz import pipe, get_in, curry
from toolz.curried import pluck

from repository.json_repository import read_json

BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = "5d06f90c326d9c6fcad20324c803ec76"


def get_targets_cities():
    all_targets = read_json("../Data/targets.json")
    return pipe(all_targets, partial(pluck, 'Target City'), list)

@curry
def api_request(url, params) -> Optional[Dict[str, Any]]:
    try:
        return pipe(
            requests.get(url, params=params),
            lambda response: response.raise_for_status() or response.json()
        )
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


get_full_weather_data = api_request(BASE_URL)


def get_target_time(target_time: Optional[datetime] = None) -> datetime:
    return target_time or (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))


def find_closest_forecast(forecasts, target_time) -> Dict[str, Any]:
    target_timestamp = int(target_time.timestamp())
    return min(forecasts, key=lambda x: abs(x['dt'] - target_timestamp))


def extract_location(data) -> Dict[str, float]:
    return {
        "lat": get_in(['city', 'coord', 'lat'], data),
        "lon": get_in(['city', 'coord', 'lon'], data)
    }


def extract_weather(forecast) -> Dict[str, Any]:
    return {
        "weather": get_in(['weather', 0, 'main'], forecast),
        "clouds": get_in(['clouds', 'all'], forecast),
        "wind_speed": get_in(['wind', 'speed'], forecast)
    }


def extract_weather_info(full_data, target_time: Optional[datetime] = None)\
        -> Optional[Dict[str, Any]]:
    if not full_data or 'list' not in full_data:
        return None

    return {
        "location": extract_location(full_data),
        "weather": pipe(
            full_data['list'],
            partial(find_closest_forecast, target_time=get_target_time(target_time)),
            extract_weather
        )
    }


def get_weather_for_midnight(api_key, city, target_time: Optional[datetime] = None)\
        -> Optional[Dict[str, Any]]:
    return pipe(
        get_full_weather_data({'q': city, 'appid': api_key, 'units': 'metric'}),
        partial(extract_weather_info, target_time=target_time)
    )


def write_to_json(data, filename) -> None:
    """Writes data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def collect_weather_data(cities) -> Dict[str, Any]:
    """Collects weather data for a list of cities."""
    return pipe(
        cities,
        lambda cities: map(partial(get_weather_for_midnight, API_KEY), cities),
        lambda data: {city: weather for city, weather in zip(cities, data) if weather}
    )


def save_weather_data_to_json(cities, filename: str = 'weather_data.json') -> None:
    """Collects weather data and saves it to a JSON file."""
    pipe(
        cities,
        collect_weather_data,
        partial(write_to_json, filename=filename)
    )

def write_cities_data_to_json():
    cities = get_targets_cities()
    cities = pipe(cities, partial(filter, lambda x: x != "Gaza City"), list)
    save_weather_data_to_json(cities)

# write_cities_data_to_json()