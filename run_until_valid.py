import subprocess
import time

def generate_until_valid():
    while True:
        print("Generiere neue Fahrzeugdaten...")
        
        
        subprocess.run(["python", "generate_vehicle_data.py"])

        try:
            
            print("Führe Tests aus...")
            result = subprocess.run(
                ["pytest", "test_vehicle_generator.py", "--maxfail=1", "--disable-warnings", "-q"],
                check=True  
            )
            
            
            if result.returncode == 0:
                print("Alle Tests erfolgreich! Daten sind korrekt.")
                break  
                
        except subprocess.CalledProcessError:
            print("Test fehlgeschlagen. Generiere neue Daten...")
            time.sleep(2)  

if __name__ == "__main__":
    generate_until_valid()
