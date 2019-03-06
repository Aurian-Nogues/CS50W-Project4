from django.shortcuts import render, redirect
import requests
import json
from pprint import pprint
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse

def index(request):
    #if user is not conntected send to login page
    if not request.user.is_authenticated:
        return render(request, "stocks/login.html", {"message": None})

    return HttpResponseRedirect(reverse("dashboard"))

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "stocks/login.html", {"message": "Invalid credentials."})

def createAccount(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # log the user in
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()

    return render(request, "stocks/create_account.html", {'form': form})

def logout_view(request):
    logout(request)
    return render(request, "stocks/login.html", {"message": "Logged out."})


def dashboard(request):
    #if user is not conntected send to login page
    if not request.user.is_authenticated:
        return render(request, "stocks/login.html", {"message": None})

    context = {
    }
    return render(request, "stocks/dashboard.html", context)




def ideas(request):
    #if user is not conntected send to login page
    if not request.user.is_authenticated:
        return render(request, "stocks/login.html", {"message": None})

    context = {
    }
    return render(request, "stocks/ideas.html", context)

def cut_off_numbers_from_dict_keys(dictionary):
    result = {}
    for key, val in dictionary.items():
        new_key = key.split('. ')[1]
        result[new_key] = val
    return result

assert cut_off_numbers_from_dict_keys({
    "1. symbol": "AAPL",
    "2. name": "Apple Inc.",
    "3. type": "Equity",
    "4. region": "United States",
    "5. marketOpen": "09:30",
    "6. marketClose": "16:00",
    "7. timezone": "UTC-05",
    "8. currency": "USD",
    "9. matchScore": "0.8889"
}) == {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "type": "Equity",
    "region": "United States",
    "marketOpen": "09:30",
    "marketClose": "16:00",
    "timezone": "UTC-05",
    "currency": "USD",
    "matchScore": "0.8889"
}

def trade(request):
    #if user is not conntected send to login page
    if not request.user.is_authenticated:
        return render(request, "stocks/login.html", {"message": None})

    if request.method == 'POST':
        #get stock name and build alphavantage API query
        stock = request.POST["stock-name"]
        api_query = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + stock + "&apikey=7ZON9TG94BAELGBM&datatype=json"
        #get response and put it in Json format
        response = requests.get(api_query)
        data = dict(response.json())
        data = [cut_off_numbers_from_dict_keys(item) for item in data['bestMatches']]
        pprint(data)
        #length = len(data['bestMatches'])
        #for i in range (0,length):
        #    print(data['bestMatches'][i]['2. name'])
        #pprint(data)
        #print(data['bestMatches'][0]['2. name'])
        context = {
            "data": data,
        }
        return render(request, "stocks/select_stock.html", context)


    context = {
    }
    return render(request, "stocks/select_stock.html", context)

def build_trade(request, ticker):

    context = {
        "ticker": ticker
    }

    return render(request, "stocks/build_trade.html", context)



# api key 7ZON9TG94BAELGBM