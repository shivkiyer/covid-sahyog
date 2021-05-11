from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def launch_app(request):
    return render(request, 'index.html', {})


def request_help(request):
    return render(request, 'request_help.html', {})


def offer_help(request):
    return render(request, 'offer_help.html', {})


def about_us(request):
    return render(request, 'about_us.html', {})
