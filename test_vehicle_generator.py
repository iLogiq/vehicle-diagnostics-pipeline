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

    rpm_thresholds_ice = {
        (0, 0): (700, 900),       
        (1, 30): (1000, 2000),     
        (31, 60): (1500, 3000),    
        (61, 100): (2200, 4000),   
        (101, 140): (3000, 5000),  
        (141, 180): (4000, 6000),  
        (181, 240): (5000, 6500),  
    }

    rpm_thresholds_tesla = {
        (0, 0): (0, 200),      
        (1, 30): (100, 500),   
        (31, 60): (300, 1200), 
        (61, 100): (1500, 3000),
        (101, 140): (3500, 5500),
        (141, 180): (6000, 8000),
        (181, 240): (8000, 12000), 
    }

  
    def get_rpm_range(vehicle, speed):
        if vehicle == 'TESLA-789':
            for (low, high), (min_rpm, max_rpm) in rpm_thresholds_tesla.items():
                if low <= speed <= high:
                    return min_rpm, max_rpm
        else:        
            for (low, high), (min_rpm, max_rpm) in rpm_thresholds_ice.items():
                if low <= speed <= high:
                    return min_rpm, max_rpm
        return None, None 

    
    for entry in data:
        speed = int(entry["speed_kmh"])
        rpm = int(entry["rpm"])
        vehicle = entry['vehicle_id']
        min_rpm, max_rpm = get_rpm_range(vehicle, speed)
        
        assert min_rpm is not None and max_rpm is not None, f"Kein RPM-Bereich gefunden für {vehicle} bei {speed} km/h"
        assert min_rpm <= rpm <= max_rpm, f"RPM {rpm} ist ungültig für {vehicle} bei {speed} km/h"


def test_temperature_requires_rpm_and_speed():
    data = load_data_from_csv()
    
    def is_realistic_temperature(vehicle, rpm, speed_kmh, engine_temp_c):

        if vehicle == 'TESLA-789':
            if rpm < 3000:
                assert 20 <= engine_temp_c <= 50, f"Temperatur {engine_temp_c} für {vehicle} bei {rpm} RPM ist ungültig"
            elif rpm < 6000:
                assert 50 <= engine_temp_c <= 80, f"Temperatur {engine_temp_c} für {vehicle} bei {rpm} RPM ist ungültig"
            else:
                assert 80 <= engine_temp_c <= 120, f"Temperatur {engine_temp_c} für {vehicle} bei {rpm} RPM ist ungültig"
        else:
            if rpm < 3000:
                assert 30 <= engine_temp_c <= 60, f"Temperatur {engine_temp_c} für {vehicle} bei {rpm} RPM ist ungültig"
            elif rpm < 5000:
                assert 60 <= engine_temp_c <= 90, f"Temperatur {engine_temp_c} für {vehicle} bei {rpm} RPM ist ungültig"
            else:
                assert 90 <= engine_temp_c <= 120, f"Temperatur {engine_temp_c} für {vehicle} bei {rpm} RPM ist ungültig"

    for entry in data:
        speed = int(entry["speed_kmh"])
        rpm = int(entry["rpm"])
        vehicle = entry['vehicle_id']
        engine_temp_c = int(entry['engine_temp_c'])
        is_realistic_temperature(vehicle, rpm, speed, engine_temp_c)
        
        if speed > 180:
            assert engine_temp_c >= 80, f"Temperatur {engine_temp_c} für {vehicle} bei {speed} km/h ist zu niedrig"
        elif speed > 100:
            assert engine_temp_c >= 50, f"Temperatur {engine_temp_c} für {vehicle} bei {speed} km/h ist zu niedrig"
        else:
            assert engine_temp_c >= 30, f"Temperatur {engine_temp_c} für {vehicle} bei {speed}  km/h ist zu niedrig"

    
def test_error_codes():
    data = load_data_from_csv()
    
    for entry in data:
        error_codes = entry['error_code'].split(', ') if entry['error_code'] else []
        speed = int(entry['speed_kmh'])
        rpm = int(entry['rpm'])
        engine_temp = int(entry['engine_temp_c'])
        fuel_level = int(entry['fuel_level_percent'])
        vehicle = entry['vehicle_id']

        for error in error_codes:
            if error == "P0300":
                assert speed < 150, f"P0300 erkannt, aber Geschwindigkeit {speed} km/h ist zu hoch bei {vehicle}"
            elif error == "P0171":
                assert engine_temp < 110, f"P0171 erkannt, aber Motortemperatur {engine_temp}°C ist zu hoch bei {vehicle}"
            elif error == "P0420":
                pass
            elif error == "P0500":
                assert speed == 0, f"P0500 erkannt, aber Geschwindigkeit {speed} km/h wird gemessen bei {vehicle}"
            elif error == "P0128":
                assert engine_temp < 90, f"P0128 erkannt, aber Motortemperatur {engine_temp}°C ist zu hoch bei {vehicle}"
            elif error == "P0455":
                assert fuel_level < 90, f"P0455 erkannt, aber Tankfüllstand {fuel_level}% ist sehr hoch bei {vehicle}"
                      