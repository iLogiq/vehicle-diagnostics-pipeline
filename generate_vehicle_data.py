import csv
from datetime import datetime
import random

def generate_vehicle_data():
    vehicles = ['BMW-123', 'AUDI-456', 'TESLA-789']
    error_codes = ["P0300", "P0171", "P0420", "P0500", "P0128", "P0455"]
    data = []

    for vehicle in vehicles:
        entry = {
            "timestamp": str(datetime.now()),
            "vehicle_id": vehicle,
            "speed_kmh": random.randint(1, 240),
            "engine_temp_c": random.randint(20, 120),
            "rpm": random.randint(700, 6500) if vehicle != 'TESLA-789' else random.randint(0, 15000),
            "error_code": ', '.join(random.sample(error_codes, k=random.randint(0, 2))),
            "fuel_level_percent": random.randint(5, 95)
        }
        data.append(entry)

    return data


def write_to_csv(data, filename='vehicle_data.csv'):
    with open(filename, mode='w', newline='') as file:
        
        fieldnames = ["timestamp", "vehicle_id", "speed_kmh", "engine_temp_c", "rpm", "error_code", "fuel_level_percent"]
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for entry in data:
            writer.writerow(entry)


vehicle_data = generate_vehicle_data()


write_to_csv(vehicle_data)
      