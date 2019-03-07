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

    #get current user and find his open trades
    user=request.user
    trades = Trade_idea.objects.all().filter(user=user, status="open")
        
    #for each open trade 
    for trade in trades:

        #get the ticker and make a query to the api
        ticker = trade.ticker
        api_query = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + ticker + "&apikey=7ZON9TG94BAELGBM"
        response = requests.get(api_query)
        data = dict(response.json())

        #remove numbers from dictionnary so keys are accessible
        data = data['Global Quote']
        data = cut_off_numbers_from_dict_keys(data)

        #get necessary data and calculate upside and performance. Convert them to a string with % to print nicely in html table
        current_price = float(data['price'])
        open_price = float(trade.open_price)
        target_price = float(trade.target_price)
        upside = (current_price / target_price -1 ) * 100
        upside = str(round(upside, 2)) + '%'
        performance = (current_price / open_price -1 ) * 100
        performance = str(round(performance, 2)) + '%'

        #write it in database
        trade.current_price = current_price
        trade.performance = performance
        trade.upside = upside
        trade.save()

    trades = Trade_idea.objects.all().filter(user=user, status="open")

    context = {
        "trades": trades,
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
    data = dict(response.json())

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
    
        user=request.user
        name = request.POST.get('name')
        ticker = request.POST.get('ticker')
        price = request.POST.get('price')
        message = request.POST.get('message')
        date = datetime.date.today()
        target = request.POST.get('target')
        status="open"
        entry = Trade_idea(user=user, ticker=ticker, name=name, open_price=price, message=message, open_date=date, status=status, target_price=target)
        entry.save()

        context = {
        
        }
        return render(request, "stocks/dashboard.html", context)

    else:
        raise Http404



# api key 7ZON9TG94BAELGBM