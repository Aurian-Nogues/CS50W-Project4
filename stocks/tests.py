from django.test import TestCase
from .models import Trade_idea
import requests, json, datetime
from .views import cut_off_numbers_from_dict_keys


# Create your tests here.
class StocksTestCase(TestCase):

    def setUp(self):
        # Create new trade ideas
            entry = Trade_idea(user="Warren", ticker="AAPL", name="Apple", open_price=175, message="Undervalued", open_date="2019-03-07", status="open", target_price=180)
            entry.save()
            entry = Trade_idea(user="George", ticker="GOOG", name="Alphabet", open_price=1150.53, message="I like it", open_date="2018-03-07", status="open", target_price=1200)
            entry.save()
        
    
    def test_new_ideas(self):
        #test if new trade ideas can be added to database
        ideas = Trade_idea.objects.all()
        self.assertEqual(ideas.count(), 2)

    def test_api_queries(self):
        #make a request to api endpoint and check that length of returned dictionary hasn't changed. 

        #https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=7ZON9TG94BAELGBM
        ticker = "AAPL"
        api_query = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + ticker + "&apikey=7ZON9TG94BAELGBM"
        response = requests.get(api_query)
        data = dict(response.json())
        expected = {'Global Quote': {'01. symbol': 'AAPL', '02. open': '173.8700', '03. high': '174.4400', '04. low': '172.0347', '05. price': '172.4300', '06. volume': '6506040', '07. latest trading day': '2019-03-07', '08. previous close': '174.5200', '09. change': '-2.0900', '10. change percent': '-1.1976%'}}
        
        assert len(data) == len(expected)

    def test_close_trade(self):
        #test if trade can be closed successfully then be identified as a closed trade
        user="Warren"
        ticker="AAPL"
        open_price = 175
        open_date = "2019-03-07"
        trade = Trade_idea.objects.all().get(user=user, status="open", ticker=ticker, open_price=open_price, open_date=open_date)
        
        close_date = datetime.date.today()
        trade.status = "closed"
        trade.close_price = 180
        trade.close_date = close_date
        trade.performance = "15%"
        trade.save()

        result = Trade_idea.objects.all().filter(status="closed")

        assert len(result) == 1


    def test_cutoff_function(self):
        #test if function to cut numbers from alphavantage response returns expected dict format
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

