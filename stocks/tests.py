from django.test import TestCase
from .models import Trade_idea



# Create your tests here.
class StocksTestCase(TestCase):

    def setUp(self):
        # Create new trade ideas
            entry = Trade_idea(user="Warren", ticker="AAPL", name="Apple", open_price=175, message="Undervalued", open_date="2019-03-07", status="open")
            entry.save()
            entry = Trade_idea(user="George", ticker="GOOG", name="Alphabet", open_price=1150.53, message="I like it", open_date="2018-03-07", status="open")
            entry.save()
    
    def test_new_ideas(self):
        ideas = Trade_idea.objects.all()
        self.assertEqual(ideas.count(), 2)

