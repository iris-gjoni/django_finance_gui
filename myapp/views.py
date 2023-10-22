from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
import csv


class HelloWorld(View):
    def get(self, request):
        return HttpResponse("Hello, World!")


class PageTwo(View):
    def get(self, request):
        return HttpResponse("page two !")


def PageThree(request):
    return render(request, 'myapp/Navigations.html')


def GraphPage(request):
    return render(request, 'myapp/graphing.html')


def my_view(request):
    dates, closes = read_csv_data('C:/quant/historicalStockPrices/historical_AAPL.csv')
    return render(request, 'myapp/graphing.html', {
        'dates': dates,
        'closes': closes
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

