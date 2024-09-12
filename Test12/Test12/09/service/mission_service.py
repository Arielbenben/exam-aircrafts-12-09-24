import math
from toolz import partial, pipe, first
from toolz.curried import pluck
from repository.csv_repository import write_missions_to_csv

from repository.json_repository import read_json
from service.api_service import get_targets_cities


tel_aviv_location = {'lat': 32.0852997, 'lon': 34.7818064}


# Function to calculate the distance between two coordinates using the Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):

    r = 6371.0  # Radius of the Earth in kilometers

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon /
    2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = r * c
    return distance

def weather_score (weather):

    if weather['weather'] == "Clear":
        return 1.0 # Best condition

    elif weather['weather'] == "Clouds":
        return 0.7 # clouds are moderate

    elif weather['weather'] == "Rain":
        return 0.4 # Rainy weather

    elif weather['weather'] == "Stormy":
        return 0.2 # Stormy weather is least favorable

    else:
        return 0 # Unfavorable condition


def get_all_targets():
    return read_json("../Data/targets.json")


def get_piority(city):
    all_targets = read_json("../Data/targets.json")
    return pipe(all_targets, partial(filter, lambda x: x["Target City"] == city),
                partial(pluck, 'Priority'), first)


def get_all_pilots_details():
    return read_json("../Data/pilots.json")


def get_all_pilots():
    return pipe(
        get_all_pilots_details(),
        partial(pluck, "name"),
        list
    )

def get_al_aircrafts_details():
    return read_json("../Data/aircrafts.json")


def get_location_for_city(city):
    return pipe(
        read_json("../service/weather_data.json"),
        lambda x: x[city]["location"]
    )

def check_distance_for_city(city):
    target_location = get_location_for_city(city)
    return haversine_distance(tel_aviv_location["lat"], tel_aviv_location["lon"],
                                  target_location["lat"], target_location['lon'])

def get_weather_for_city(city):
    return pipe(
        read_json("../service/weather_data.json"),
        lambda x: x[city]["weather"]
    )

def check_time_to_attack(target, aircraft):
    distance = check_distance_for_city(target)
    return distance / aircraft["speed"]

def check_prucent_to_distance(distance, aircraft):
    check = distance / aircraft['fuel_capacity']
    return 20 if check <= 1 else 100 * check / 20


def get_average_skill():
    return pipe(
        get_all_pilots_details(),
        partial(pluck, 'skill'),
        partial(map, lambda x: int(x)),
        list,
        lambda x: sum(x) / len(x))


def check_grade_to_pilot(pilot):
    all_pilots = get_all_pilots_details()
    average_skill = get_average_skill()
    pilot_skill_compare = average_skill / pilot["skill"]
    return 25 if pilot_skill_compare <= 1 else pilot_skill_compare * 100 / 25


def check_prucent_weather(city):
    return pipe(get_weather_for_city(city), weather_score, lambda x: x * 20)

def check_prucent_time(city, aircraft):
     time_to_attack = check_time_to_attack(city, aircraft)
     return 10 if time_to_attack <= 1 else time_to_attack * 20 / 10


def mission_fit_score(target, pilot, aircraft):
    distance = check_distance_for_city(target['Target City'])
    distance_prucent = check_prucent_to_distance(distance, aircraft)
    pilot_prucent = check_grade_to_pilot(pilot)
    weather_prucent = check_prucent_weather(target['Target City'])
    time_prucent = check_prucent_time(target['Target City'], aircraft)
    grade = distance_prucent + pilot_prucent + weather_prucent + time_prucent
    return grade


def get_weather_condition(city):
    return get_weather_for_city(city)["weather"]


def create_mission(target, pilot, aircraft):
    return {'target city': target['Target City'], 'piority': get_piority(target['Target City']), 'pilot': pilot['name'],
               'aircraft': aircraft['type'], 'distance': check_distance_for_city(target['Target City']),
               'weather condition': get_weather_condition(target['Target City']), 'pilot skill': pilot['skill'],
               'aircraft speed': aircraft['speed'], 'fuel capacity': aircraft['fuel_capacity'],
               'mission fit score': mission_fit_score(target, pilot, aircraft)}


def create_all_missions(all_targets, all_pilots, all_aircraft):
    missions = []
    for target in all_targets:
        for pilot in all_pilots:
            for aircraft in all_aircraft:
                missions.append(create_mission(target, pilot, aircraft))
    return missions

all_pilots = get_all_pilots_details()
all_targets = get_all_targets()
all_aircrafts = get_al_aircrafts_details()

def turn_on_create_missions():
    all_missions = create_all_missions(all_targets, all_pilots, all_aircrafts)
    return write_missions_to_csv(all_missions)

