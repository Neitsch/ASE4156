"""
Views for trading
"""
from django.http import HttpResponse
from stocks.models import InvestmentBucket


def test(request):
    """
    Dev method for buckets
    """
    i = InvestmentBucket.objects.all()
    t = []
    for x in i:
        t.append(x.get_stock_configs())
    return HttpResponse(t)
