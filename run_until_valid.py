import subprocess
import time

def generate_until_valid():
    while True:
        print("Generiere neue Fahrzeugdaten...")
        
        # Fahrzeugdaten generieren
        subprocess.run(["python", "generate_vehicle_data.py"])

        try:
            # Tests ausführen
            print("Führe Tests aus...")
            result = subprocess.run(
                ["pytest", "test_vehicle_generator.py", "--maxfail=1", "--disable-warnings", "-q"],
                check=True  # Nur eine Ausnahme, wenn der Exit-Status ungleich 0 ist
            )
            
            # Überprüfe den Exit-Status von pytest (der Wert muss 0 sein)
            if result.returncode == 0:
                print("Alle Tests erfolgreich! Daten sind korrekt.")
                break  # Alle Tests bestanden, Schleife beenden
                
        except subprocess.CalledProcessError:
            print("Test fehlgeschlagen. Generiere neue Daten...")
            time.sleep(2)  # Pausieren, bevor neue Daten generiert werden

if __name__ == "__main__":
    generate_until_valid()
