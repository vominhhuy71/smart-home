import requests
import json
import time
import sys

while True:
    temp = requests.get("http://46.101.183.30:5000/info/thermistor")
    data = temp.json()
    print(data)
    sys.stdout.flush()
    time.sleep(1)