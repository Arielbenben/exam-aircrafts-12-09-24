import json
from operator import itemgetter

from toolz.curried import partial, pipe

from models.aircraft import Aircraft
from models.pilot import Pilot
import os


def read_json(path):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # is_file = os.path.isfile("../Data/targets.json")
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return []

def create_json_file(json_var, name):
    json_str = json.dumps(json_var)
    json_file = open(" ./Data/" + name + ".json", "w")
    json_file.write(json_str)
    json_file.close()


def convert_from_json_to_pilot(json):
    return Pilot(
        name = json["name"],
        skill=json["skill"]
    )

def convert_from_json_to_target(json):
    return  {"target_city": json["name"], "priority": json["Priority"] }


def convert_from_json_to_aircraft(json):
    return Aircraft(
        type = json["type"],
        speed=json["speed"],
        fuel_capacity = json["fuel_capacity"]
    )

def get_data():
    all_targets = read_json("../Data/targets.json")
    all_targets_city = pipe(all_targets, partial(map, itemgetter('Target City')), list)





# print(a)
# print(pipe(
#     a,
#     partial(map, lambda x: x['list']),
#     partial(filter, lambda x: x['dt_txt'] == '2024-09-13 00:00:00'),
#     list
# ))