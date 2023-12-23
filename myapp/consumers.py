import csv
import os
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from myapp.util_dir.message_types import message_type_string, add_to_graph, load_graph, get_new_csv_data, file_path
import myapp.util_dir.YahooFinUtil as fin_util


class DashConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('connection')
        await self.accept()
        self.loop_task = asyncio.create_task(self.check_for_updates("c:/quant/shared_data/share.csv"))

    async def disconnect(self, code):
        print(f'connection closed: {code}')
        self.loop_task.cancel()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_type = text_data_json[message_type_string]
        if message_type == load_graph:
            await self.do_load_graph(text_data_json)

        if message_type == add_to_graph:
            print("add to graph not implemented here")

        if message_type == get_new_csv_data:
            ticker = text_data_json["ticker"]
            final_file_path = file_path + "historical_" + ticker + ".csv"
            fin_util.append_new_data(ticker, final_file_path)

    async def do_load_graph(self, text_data_json):
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

    async def check_for_updates(self, file_path):
        while True:
            updates = await self.get_updates(file_path)

            if updates:
                # Send updates to the WebSocket client
                # await self.send(json.dumps(updates))
                print("updates received")

            await asyncio.sleep(5)  # Waits for 5 seconds before next check

    async def get_updates(self, file_path):
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                print(row)
            return row


def read_all_csv_data(days, ticker):
    # todo implement days and ticker filtering
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
        # if name == ticker:
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
