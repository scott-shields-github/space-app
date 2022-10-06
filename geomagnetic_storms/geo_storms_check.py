# import requests
# import json

# API_KEY = "DEMO_KEY"

# def main():
#     r = requests.get(f"https://api.nasa.gov/DONKI/GST?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd&api_key={API_KEY}")
#     response = json.loads(r.content)[0]
#     print(response["linkedEvents"])

# if __name__ == '__main__':
#     main()

import requests
from datetime import datetime, timedelta
from constants import API_KEY, NASA_API_ENDPOINT

time_now = datetime.utcnow()
time_start = time_now - timedelta(days=30)


def main():
    response = requests.get(f"{NASA_API_ENDPOINT}?startDate={time_start}&endDate={time_now}&api_key={API_KEY}").json()[0]
    link = response["link"]
    kpIndex = response["allKpIndex"][0]["kpIndex"]

    if datetime.strptime(response["startTime"], "%Y-%m-%dT%H:%MZ").day == time_now.day:
        print(f"Warning! There is a Geomagnetic Storm Today! kpIndex: {kpIndex}")
    else:
        print("No Geomagnetic Storms Today! Phew!")

    print(f"Link for the last Geomagnetic Storm event: {link}")

if __name__ == '__main__':
    main()