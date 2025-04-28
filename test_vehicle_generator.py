import csv
import pytest


def load_data_from_csv(filename='vehicle_data.csv'):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def test_speed_within_limits():
    data = load_data_from_csv()
    for entry in data:
        speed = int(entry["speed_kmh"])
        assert 0 <= speed <= 240, f"Geschwindigkeit {speed} km/h ist ungültig für {entry['vehicle_id']}"
    
def test_speed_requires_rpm():
    data = load_data_from_csv()

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

    def get_rpm_range(vehicle, speed):
        vehicle_type = 'TESLA-789' if vehicle == 'TESLA-789' else 'ICE'
        rpm_range = rpm_thresholds.get(vehicle_type, {})
    
        for (low, high), (min_rpm, max_rpm) in rpm_range.items():
            if low <= speed <= high:
                print(min_rpm,max_rpm)
                return min_rpm, max_rpm
        return 0, 0 

    for entry in data:
        speed = int(entry["speed_kmh"])
        rpm = int(entry["rpm"])
        vehicle = entry['vehicle_id']
        min_rpm, max_rpm = get_rpm_range(vehicle, speed)
        
        assert min_rpm is not None and max_rpm is not None, f"Kein RPM-Bereich gefunden für {vehicle} bei {speed} km/h"
        assert min_rpm <= rpm <= max_rpm, f"RPM {rpm} ist ungültig für {vehicle} bei {speed} km/h"

def test_temperature_requires_rpm_and_speed():
    data = load_data_from_csv()

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

    def get_temperature_range(vehicle, rpm):
        
        thresholds = temperature_thresholds.get('TESLA-789' if vehicle == 'TESLA-789' else 'ICE', [])
        for rpm_limit, temp_range in thresholds:
            if rpm < rpm_limit:
                return temp_range
        return None

    for entry in data:
        speed = int(entry["speed_kmh"])
        rpm = int(entry["rpm"])
        vehicle = entry['vehicle_id']
        engine_temp_c = int(entry['engine_temp_c'])
        
        min_temp, max_temp = get_temperature_range(vehicle, rpm)
        assert min_temp <= engine_temp_c <= max_temp, f"Temperatur {engine_temp_c} für {vehicle} bei {rpm} RPM ist ungültig"
        
        if speed > 180:
            assert engine_temp_c >= 80, f"Temperatur {engine_temp_c} für {vehicle} bei {speed} km/h ist zu niedrig"
        elif speed > 100:
            assert engine_temp_c >= 50, f"Temperatur {engine_temp_c} für {vehicle} bei {speed} km/h ist zu niedrig"
        else:
            assert engine_temp_c >= 30, f"Temperatur {engine_temp_c} für {vehicle} bei {speed} km/h ist zu niedrig"

def test_error_codes():
    data = load_data_from_csv()
    
    error_checks = {
        "P0300": lambda entry: int(entry['speed_kmh']) < 150,
        "P0171": lambda entry: int(entry['engine_temp_c']) < 110,
        "P0420": lambda entry: True,  
        "P0128": lambda entry: int(entry['engine_temp_c']) < 90,
        "P0455": lambda entry: int(entry['fuel_level_percent']) < 90,
    }
    
    for entry in data:
        error_codes = entry['error_code'].split(', ') if entry['error_code'] else []
        vehicle = entry['vehicle_id']

        for error in error_codes:
            if error in error_checks:
                assert error_checks[error](entry), f"Fehler {error} erkannt, aber Bedingungen nicht erfüllt für {vehicle}"
                      
test_speed_requires_rpm()