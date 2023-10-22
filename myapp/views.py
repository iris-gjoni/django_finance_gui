from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render


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