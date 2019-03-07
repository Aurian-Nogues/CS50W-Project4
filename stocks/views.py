from django.shortcuts import render, redirect
import requests, json, datetime
from pprint import pprint
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .models import Trade_idea

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
        #protect from empty string input
        if stock == "":
            return render(request, "stocks/select_stock.html")

        api_query = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + stock + "&apikey=7ZON9TG94BAELGBM&datatype=json"
        #get response and put it in dict
        response = requests.get(api_query)
        data = dict(response.json())

        #remove numbers from dictionnary so keys are accessible
        data = [cut_off_numbers_from_dict_keys(item) for item in data['bestMatches']]

        context = {
            "data": data,
        }
        return render(request, "stocks/select_stock.html", context)

    
    context = {
    }
    return render(request, "stocks/select_stock.html", context)

def build_trade(request, ticker, name):
    #if user is not conntected send to login page
    if not request.user.is_authenticated:
        return render(request, "stocks/login.html", {"message": None})
    #build alphavantage API query
    api_query = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + ticker + "&apikey=7ZON9TG94BAELGBM"
    #get response and put it in dict
    response = requests.get(api_query)
    #pprint(response)
    data = dict(response.json())
    #remove numbers from dictionnary so entries are accessible

    #remove numbers from dictionnary so keys are accessible
    data = data['Global Quote']
    data = cut_off_numbers_from_dict_keys(data)
    pct = data['change percent']

    context = {
        "ticker": ticker,
        "data": data,
        "pct": pct,
        "name": name
    }
    return render(request, "stocks/build_trade.html", context)

def record_trade(request):
    #if user is not conntected send to login page
    if not request.user.is_authenticated:
        return render(request, "stocks/login.html", {"message": None})

    #if request is not a POST, send back to selecting a stock
    if request.method == 'GET':
        context = {

        }
        return render(request, "stocks/select_stock.html", context)

    if request.is_ajax() and request.POST:
    
        print("POST")
        user=request.user
        name = request.POST.get('name')
        ticker = request.POST.get('ticker')
        price = request.POST.get('price')
        message = request.POST.get('message')
        date = datetime.date.today()
        status="open"
        entry = Trade_idea(user=user, ticker=ticker, name=name, open_price=price, message=message, open_date=date, status=status)
        entry.save()




        context = {
        
        }

        return render(request, "stocks/dashboard.html", context)

    else:
        raise Http404



# api key 7ZON9TG94BAELGBM