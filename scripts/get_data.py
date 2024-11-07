import csv
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import mlflow
from mlflow.tracking import MlflowClient
 
os.environ["MLFLOW_REGISTRY_URI"] = "/home/den/project/mlflow/"
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("get_data_1")


class WeatherMaker:
    MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
              "october", "november", "december"]
    MONTHS_RU = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                 'октября', 'ноября', 'декабря']

    def __init__(self):
        self.weather_report = []
        self.pages_weather_report = [["date", "temp"]]
        self.html = None
        self.path = Path('/home/den/project/datasets/data.csv') 
        
    def get_html(self, url):
        self.html = requests.get(url)

    def get_content(self):
        soup = BeautifulSoup(self.html.text, "html.parser")
        items = soup.find_all("div", class_="climate-calendar-day__detailed-container-center")
        items.encoding = "utf-8"
        for item in items:
            date = item.find("h6", class_="climate-calendar-day__detailed-day").get_text().split(',')[0].split(" ")

            for i, val in enumerate(self.MONTHS_RU):
                if val in date:
                    date[1] = str(i + 1)
                    self.weather_report.append([
                        datetime.strptime(" ".join(date) + " " + str(datetime.now().year), '%d %m %Y').date().strftime(
                            "%d.%m.%Y"),
                        item.find("span", class_="temp__value temp__value_with-unit").get_text(),
                    ])

    def parse(self):

        date_from = datetime.now() - timedelta(days=10)
        date_to = datetime.now()

        for month in range(date_from.month - 1, date_to.month):
            URL = f'https://yandex.ru/pogoda/month/{self.MONTHS[month]}?lat=56.829472&lon=60.532538&via=ms'
            self.get_html(URL)
            if self.html.status_code == 200:
                self.get_content()
                for elem in self.weather_report:
                    if elem not in self.pages_weather_report:
                        if date_from <= datetime.strptime(elem[0], "%d.%m.%Y") <= date_to:
                            self.pages_weather_report.append(elem)
                if self.path.is_file():
                    print(self.pages_weather_report)
                    with open(self.path, 'a', encoding="utf-8", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows([self.pages_weather_report[-1]])
                else:
                    with open(self.path, 'a', encoding="utf-8", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(self.pages_weather_report)

            else:
                print("Error")
        return self.pages_weather_report

weather = WeatherMaker().parse()

with mlflow.start_run():
    mlflow.log_param("URL", 'https://yandex.ru/pogoda/month/{self.MONTHS[month]}?lat=56.829472&lon=60.532538&via=ms')
    mlflow.end_run()
