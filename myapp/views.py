import json
import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
import csv


class HelloWorld(View):
    def get(self, request):
        return HttpResponse("Hello, World!")


class PageTwo(View):
    def get(self, request):
        return HttpResponse("page two !")


def Async_page(request):
    print(f'async got: {request}')

    if request.method == 'POST':
        print('POST mesage')
    return render(request, 'myapp/async_page.html', {})


def PageThree(request):
    return render(request, 'myapp/Navigations.html')


def GraphPage(request):
    return render(request, 'myapp/graphing.html')


def my_view(request):
    serialized_data = []

    if request.method == "POST":
        print(request.POST)
        ticker = request.POST.get('dataSelect')
        time = request.POST.get('timeSelect')
        datasets = read_all_csv_data(time, ticker)
        serialized_data = [
            {
                'name': entry.name,
                'dates': entry.dates,
                'closes': entry.closes
            }
            for entry in datasets
        ]

    return render(request, 'myapp/graphing.html', {
        'data': json.dumps(serialized_data),
    })


def read_csv_data(filename):
    dates = []
    closes = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row['Date'])
            closes.append(float(row['Close']))

    return dates, closes


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
