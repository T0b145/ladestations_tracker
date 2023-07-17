import requests
import csv
from datetime import datetime
import pytz

 # Specify the CSV file path (existing or new)
csv_file_path = "data.csv"

stationen = [
    {"name":"Platanenstr. 11", "id":"5y35yn"},
    {"name":"Lindenstraße 71", "id":"z228j8"},
    {"name":"Ackerstraße 131", "id":"zn686k"},
    {"name":"Ackerstraße Schnelllader", "id":"2jqwpp"},
    {"name":"Hermannstr.22a", "id":"jqmy9n"},
    {"name":"Birkenstraße 47a ", "id":"gjje3n"}
    ]

def ladestation_request(id):
    session = requests.Session()
    session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "authority": "api.chargefinder.com",
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,de;q=0.8",
    "origin": "https://chargefinder.com",
    "referer": "https://chargefinder.com/",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
    })

    url = f"https://api.chargefinder.com/status/{id}"
    response = session.get(url)
    return response

    
for st in stationen:
    response = ladestation_request(st["id"])
    if response.status_code == 200:
        json_data = response.json()
        
        germany_tz = pytz.timezone('Europe/Berlin')
        request_datetime = datetime.now(germany_tz)

        for station in json_data:
            # Open the CSV file in append mode
            with open(csv_file_path, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Station_name"]+["Station_id"]+["Request Datetime"] + list(station.keys()))

                # Check if the file is empty and write the header row
                if file.tell() == 0:
                    writer.writeheader()

                # Write the JSON data as a new row in the CSV file
                station["Request Datetime"] = request_datetime
                station["Station_name"]=st["name"]
                station["Station_id"]=st["id"]
                writer.writerow(station)
    else:
        print (f"{id}: Request failed")