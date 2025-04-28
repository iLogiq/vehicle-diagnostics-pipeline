import csv
from datetime import datetime
import random


rpm_thresholds = {
    'ICE': {
        (0, 0): (700, 900),
        (1, 30): (1000, 2000),
        (31, 60): (1500, 3000),
        (61, 100): (2200, 4000),
        (101, 140): (3000, 5000),
        (141, 180): (4000, 6000),
        (181, 240): (5000, 6500),
    },
    'TESLA-789': {
        (0, 0): (0, 200),
        (1, 30): (100, 500),
        (31, 60): (300, 1200),
        (61, 100): (1500, 3000),
        (101, 140): (3500, 5500),
        (141, 180): (6000, 8000),
        (181, 240): (8000, 12000),
    }
}

temperature_thresholds = {
    'TESLA-789': [
        (3000, (20, 50)),
        (6000, (50, 80)),
        (float('inf'), (80, 120))  
    ],
    'ICE': [
        (3000, (30, 60)),
        (5000, (60, 90)),
        (float('inf'), (90, 120))
    ]
}

def get_rpm_range(vehicle, speed):
    vehicle_type = 'TESLA-789' if vehicle == 'TESLA-789' else 'ICE'
    rpm_range = rpm_thresholds.get(vehicle_type, {})
    
    for (low, high), (min_rpm, max_rpm) in rpm_range.items():
        if low <= speed <= high:
            return min_rpm, max_rpm
    return None, None

def get_temperature_range(vehicle, rpm):
    thresholds = temperature_thresholds.get('TESLA-789' if vehicle == 'TESLA-789' else 'ICE', [])
    for rpm_limit, temp_range in thresholds:
        if rpm < rpm_limit:
            return temp_range
    return None

def adjust_min_temp_for_speed(min_temp, speed):
    if speed > 180:
        return max(min_temp, 80)
    elif speed > 100:
        return max(min_temp, 50)
    else:
        return max(min_temp, 30)

def select_error_codes(speed, rpm, temp):
    error_conditions = [
        (rpm >= 6300, ["P0300", "P0420"]),
        (temp > 100, ["P0128"]),
        (speed > 200, ["P0500"])
    ]

    possible_errors = [error for condition, errors in error_conditions if condition for error in errors]

    if not possible_errors or random.random() < 0.1:
        return random.choice(["P0171", ""])

    return random.choice(possible_errors)


def generate_vehicle_data():
    vehicles = ['BMW-123', 'AUDI-456', 'TESLA-789']
    error_codes = ["P0300", "P0171", "P0420", "P0128", "P0455"]
    data = []
    
    for vehicle in vehicles:
        speed = random.randint(0, 240)
        min_rpm, max_rpm = get_rpm_range(vehicle, speed)
        
        rpm = random.randint(min_rpm, max_rpm) if min_rpm and max_rpm else 0
        

        temp_range = get_temperature_range(vehicle, rpm)
        if temp_range:
            min_temp, max_temp = temp_range
            min_temp = adjust_min_temp_for_speed(min_temp, speed)
            if random.random() < 0.9:
                engine_temp_c = random.randint(min_temp, max_temp)
            else:
            
                if random.random() < 0.5:
                    engine_temp_c = min_temp - random.randint(5, 15)  
                else:
                    engine_temp_c = max_temp + random.randint(5, 20) 
        else:
            engine_temp_c = random.randint(20, 120)

        error_code = select_error_codes(speed, rpm, engine_temp_c)

        entry = {
            "timestamp": str(datetime.now()),
            "vehicle_id": vehicle,
            "speed_kmh": speed,
            "engine_temp_c": engine_temp_c,
            "rpm": rpm,
            "error_code": error_code,
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
      
