import serial
import requests
import json

# Configuration
SERIAL_PORT = 'COM7'  # 🔁 Remplace par le port correct (ex. /dev/ttyUSB0 sous Linux)
BAUD_RATE = 115200
API_URL = 'http://localhost:3000/api/gps'  # L’API Flask sur ton PC

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Lecture depuis {SERIAL_PORT}...")
        
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    print(f"Reçu : {line}")
                    # ⚠️ Si tu envoies du JSON directement depuis l’ESP, tu peux utiliser :
                    data = json.loads(line)  # Ex : {"lat": 36.73, "lon": 3.26}
                    
                    # Envoie vers Flask
                    r = requests.post(API_URL, json=data)
                    print(f"POST {r.status_code}")
                except json.JSONDecodeError:
                    print("⚠️ Donnée non JSON ignorée")
    except serial.SerialException as e:
        print(f"Erreur série : {e}")

if __name__ == '__main__':
    main()
