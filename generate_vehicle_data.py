import csv
from datetime import datetime
import random
import time

def generate_vehicle_data():
    while True:
        time.sleep(3)
        vehicle = ['BMW-123', 'AUDI-456', 'TESLA-789']
        error_codes = ["P0300", "P0171", "P0420", "P0500", "P0128", "P0455", "U0100"]

        toWrite = [
            ["timestamp", "vehicle_id", "speed_kmh", "engine_temp_c", "rp", "error_code", "fuel_level_percent"]
        ]

        for v in vehicle:
            timestamp = str(datetime.now())
            speed = random.randint(1, 240)
            engine_temp = random.randint(20, 120)
            rpm = random.randint(700, 6500) if v != 'TESLA-789' else random.randint(0, 15000)  
            error_code = ', '.join(random.sample(error_codes, k=random.randint(0, 2)))  
            fuel_level = random.randint(5, 100)
            toWrite.append([timestamp, v, speed, engine_temp, rpm, error_code, fuel_level])

        for entry in toWrite:
            print(entry)

        return toWrite


file = open('vehicle_data.csv', 'w') 

with file:
    writer = csv.writer(file)

    for row in generate_vehicle_data():
        writer.writerow(row)