"""
Views for trading
"""
from django.http import HttpResponse
from stocks.models import InvestmentBucket


def test(request):
    """
    Dev method for buckets
    """
    investments = InvestmentBucket.objects.all()
    templist = []
    for investment in investments:
        templist.append(investment.get_stock_configs())
    return HttpResponse(templist)
