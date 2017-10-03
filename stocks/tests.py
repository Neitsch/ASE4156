from .models import Stock, DailyStockQuote
from django.test import TestCase


class StocksViewTests(TestCase):
    def test_api_for_real_stock(self):
        ticker = "googl"
        name = "Google"
        r = self.client.post('/stocks/addstock/',
                             {'name': name, 'ticker': ticker})
        self.assertEqual(r.status_code, 200)
        data = Stock.objects.all()
        self.assertEqual(len(data), 1)

    def test_api_for_invalid_ticker(self):
        ticker = "xxx"
        name = "Julian"
        r = self.client.post('/stocks/addstock/',
                             data={'name': name, 'ticker': ticker})
        self.assertEqual(r.status_code, 200)
        data = DailyStockQuote.objects.all()
        self.assertEqual(len(data), 0)

    def test_api_with_invalid_call(self):
        r = self.client.get('/stocks/addstock/')
        self.assertEqual(r.status_code, 503)

    def test_fill_quote_history(self):
        ticker = "googl"
        name = "Google"
        self.client.post('/stocks/addstock/',
                             {'name': name, 'ticker': ticker})
        data = DailyStockQuote.objects.all()
        self.assertGreater(len(data), 0)
