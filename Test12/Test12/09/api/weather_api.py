import requests
from toolz import pipe, partial, first, get_in


def get_date_from_api(url):
    response = requests.request('GET', url)
    return response.json()

def get_location_from_api(city):
    return get_date_from_api(f"https://api.openweathermap.org/geo/1.0/direct?q={city}&appid=5d06f90c326d9c6fcad20324c803ec76")

def get_weather_from_api(city):
    return get_date_from_api(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=5d06f90c326d9c6fcad20324c803ec76")

# print(get_location_from_api('tel aviv')[0]['lat'])
# print(pipe(get_location_from_api("tel aviv"),
#            get_in())

# # update_weather = get_weather_from_api('paris')
# print(pipe(
#     update_weather,
#     lambda x: x['list'],
#     partial(filter, lambda x: x['dt_txt'] == '2024-09-13 00:00:00'),
#     first,
#     lambda x: x['weather'][0]['main']
# ))
#
