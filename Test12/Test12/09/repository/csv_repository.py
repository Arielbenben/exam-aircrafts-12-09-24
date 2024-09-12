import csv
from typing import List
from toolz import  pipe, partial



# def read_missins_from_csv():
#     with open('assets/missins.csv', 'r') as file:
#         csv_reader = csv.reader(file)
#         for row in csv_reader:
#             print(row)

def write_missions_to_csv(missions):
    header = ['target_city', 'priority', 'pilot', 'aircraft', 'distance', 'weather', 'pilot_skill', 'speed', 'fuel_capacity', 'fit_score']

    with open("missions.csv", mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(header)

        for mission in missions:
            writer.writerow([
                mission['target city'],
                mission['piority'],
                mission['pilot'],
                mission['aircraft'],
                mission['distance'],
                mission['weather condition'],
                mission['pilot skill'],
                mission['aircraft speed'],
                mission['fuel capacity'],
                mission['mission fit score']
            ])

            # return {'target city': target['Target City'], 'piority': get_piority(target['Target City']),
            #         'pilot': pilot['name'],
            #         'aircraft': aircraft['type'], 'distance': check_distance_for_city(target['Target City']),
            #         'weather condition': get_weather_condition(target['Target City']), 'pilot skill': pilot['skill'],
            #         'aircraft speed': aircraft['speed'], 'fuel capacity': aircraft['fuel_capacity'],
            #         'mission fit score': mission_fit_score(target, pilot, aircraft)}