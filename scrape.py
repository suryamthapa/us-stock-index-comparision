import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from db_table import db_table
import json

START_DATE = "01/01/2020"
END_DATE = "08/13/2024"

# ID used for the AJAX request to get the data
commodityType = {
    "GOLD": 8830,
    "SILVER": 8836
}

# Some needed headers to get the request working
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest'
}

# code to get snp500 data from url
# https://api.investing.com/api/financialdata/historical/166?start-date=2024-07-15&end-date=2024-08-14&time-frame=Daily&add-missing-rows=false
# the start-date and end-date should be dynamic. use START_DATE and END_DATE dynamically.
# Finally save response in snp500.json file


def get_snp500_data():
    url = f"https://api.investing.com/api/financialdata/historical/166?start-date={START_DATE}&end-date={END_DATE}&time-frame=Daily&add-missing-rows=false"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        # Save the JSON response to snp500.json file
        with open('snp500.json', 'w') as json_file:
            json.dump(res.json(), json_file, indent=4)
        print("Data saved to snp500.json")
    else:
        print(f"Failed to retrieve data: {res.status_code}")


def get_nasdaq_data():
    url = f"https://api.investing.com/api/financialdata/historical/14958?start-date={START_DATE}&end-date={END_DATE}&time-frame=Daily&add-missing-rows=false"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        # Save the JSON response to nasdaq.json file
        with open('nasdaq.json', 'w') as json_file:
            json.dump(res.json(), json_file, indent=4)
        print("Data saved to nasdaq.json")
    else:
        print(f"Failed to retrieve data: {res.status_code}")


def get_ftse100_data():
    url = f"https://api.investing.com/api/financialdata/historical/27?start-date={START_DATE}&end-date={END_DATE}&time-frame=Daily&add-missing-rows=false"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        # Save the JSON response to ftse100.json file
        with open('ftse100.json', 'w') as json_file:
            json.dump(res.json(), json_file, indent=4)
        print("Data saved to ftse100.json")
    else:
        print(f"Failed to retrieve data: {res.status_code}")


got_data = False
try:
    get_snp500_data()
    get_nasdaq_data()
    get_ftse100_data()
    got_data = True
except:
    print("Cound not get data")

if got_data:
    try:
        # code to read gold data
        snp500_data = None
        with open('snp500.json') as f:
            snp500_data = json.load(f)

        # code to read silver data
        nasdaq_data = None
        with open('nasdaq.json') as f:
            nasdaq_data = json.load(f)

        # code to read silver data
        ftse100_data = None
        with open('ftse100.json') as f:
            ftse100_data = json.load(f)

        # Iniit the database connection
        db_schema = {
            "Date": "BIGINT PRIMARY KEY",
            "SNP500": "float",
            "NASDAQ": "float",
            "FTSE100": "float",
        }

        db = db_table("Stocks", db_schema)

        # # Used to store the data so we can cleanly insert into the Database.
        prices = {}

        # for row in snp500_data.find_all('td', class_="first left bold noWrap"):
        for row in snp500_data["data"]:
            date = datetime.strptime(row["rowDate"], '%b %d, %Y').replace(
                tzinfo=timezone.utc).timestamp()
            price = str(row["last_close"]).replace(",", "")
            prices[date] = {"SNP500": price}

        for row in nasdaq_data["data"]:
            date = datetime.strptime(row["rowDate"], '%b %d, %Y').replace(
                tzinfo=timezone.utc).timestamp()
            price = str(row["last_close"]).replace(",", "")
            if date not in prices:  # Could be that there are no gold data for the current date. If so, give gold value of null
                prices[date] = {"NASDAQ": price}
            else:
                prices[date].update({"NASDAQ": price})

        for row in ftse100_data["data"]:
            date = datetime.strptime(row["rowDate"], '%b %d, %Y').replace(
                tzinfo=timezone.utc).timestamp()
            price = str(row["last_close"]).replace(",", "")
            if date not in prices:  # Could be that there are no gold data for the current date. If so, give gold value of null
                prices[date] = {"FTSE100": price}
            else:
                prices[date].update({"FTSE100": price})

        # create the
        for date in prices:
            newItem = {
                "Date": date
            }
            newItem.update(prices[date])
            db.insert(newItem)

        print("Done updating database")
    except:
        print("Cound not load data in database")
else:
    print("Data could not be fetched")
