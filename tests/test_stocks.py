"""This module is for testing stocks"""
from django.test import TestCase
from stocks.models import Stock, DailyStockQuote


class StocksViewTests(TestCase):
    """
    Testing Stocks Model
    """

    def test_api_for_real_stock(self):
        """
        Testing adding stock via endpoint, asserting stock is inserted
        """
        ticker = "googl"
        name = "Google"
        data = {'name': name, 'ticker': ticker}
        request = self.client.post('/stocks/addstock/', data)
        self.assertEqual(request.status_code, 200)
        data = Stock.objects.all()
        self.assertEqual(len(data), 1)

    def test_api_for_invalid_ticker(self):
        """
        Testing adding stock via endpoint, asserting stock is inserted but no
        data added to DailyStockQuote since ticker is invalid
        """
        ticker = "xxx"
        name = "Julian"
        data = {'name': name, 'ticker': ticker}
        request = self.client.post('/stocks/addstock/', data)
        self.assertEqual(request.status_code, 200)
        data = DailyStockQuote.objects.all()
        self.assertEqual(len(data), 0)

    def test_api_with_invalid_call(self):
        """
        Endpoint only works with POST
        """
        request = self.client.get('/stocks/addstock/')
        self.assertEqual(request.status_code, 405)

    def test_fill_quote_history(self):
        """
        Filling data for Stock
        """
        ticker = "googl"
        name = "Google"
        data = {'name': name, 'ticker': ticker}
        self.client.post('/stocks/addstock/', data)
        data = DailyStockQuote.objects.all()
        self.assertGreater(len(data), 0)
