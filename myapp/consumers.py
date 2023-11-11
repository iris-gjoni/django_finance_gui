import csv
import os

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DashConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('connection')
        await self.accept()

    async def disconnect(self, code):
        print(f'connection closed: {code}')

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        ticker = text_data_json["ticker"]
        time = text_data_json["time"]

        print(ticker)
        print(time)

        datasets = read_all_csv_data(time, ticker)
        serialized_data = [
            {
                'name': entry.name,
                'dates': entry.dates,
                'closes': entry.closes
            }
            for entry in datasets
        ]

        await self.send(text_data=json.dumps({
            'ticker': ticker,
            'time': time,
            'serialized_data': serialized_data
        }))


def read_all_csv_data(days, ticker):
    #todo implement days and ticker filtering
    datasets = []

    directory_path = 'myapp/sampledata/'
    all_files_and_directories = os.listdir(directory_path)
    only_files = [f for f in all_files_and_directories if os.path.isfile(os.path.join(directory_path, f))]
    print(only_files)

    for file_name in only_files:
        name = file_name.split('_')[1].split('.')[0]
        file_path = directory_path + file_name
        dates = []
        closes = []
        if name == ticker:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dates.append(row['Date'])
                    closes.append(float(row['Close']))
                print("name:" + name)
                datasets.append(DataEntry(name, dates, closes))

    return datasets


class DataEntry:
    def __init__(self, name, dates, closes):
        self.name = name
        self.dates = dates
        self.closes = closes