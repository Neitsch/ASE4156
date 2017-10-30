"""
Views for trading
"""
from django.shortcuts import render
from django.http import HttpResponse
from stocks.models import InvestmentBucket
from trading.models import TradingAccount, TradeBucket
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


@login_required
def account(request):
    """
    Create a trading account (only allows one trading account/user)
    """
    if request.method == "GET":
        prof = request.user.profile
        try:
            account = TradingAccount.objects.get(profile=prof)
            return HttpResponse("You already have an account.")
        except ObjectDoesNotExist:
            c = {}
            template = "create_trading_account.html"
            return render(request, template, c)
    elif request.method == "POST":
        prof = request.user.profile
        name = request.POST.get("account_name")
        account = TradingAccount(account_name=name, profile=prof)
        account.save()
        return HttpResponse("Account succesfully created.")
    else:
        return HttpResponse("Please don't sniff urls")


def get_bucket_stock_quantities():
    """
    Get a dictionary for each bucket containing tickers, quantities
    """
    all_buckets = InvestmentBucket.objects.all()
    bucket_composition_dict = {}

    for bucket in all_buckets:
        stock_list = []
        for stock in bucket.get_stock_configs():
            stock_dic = dict()
            stock_dic['stock'] = stock.stock
            stock_dic['quantity'] = stock.quantity
            stock_list.append(stock_dic)
        print(stock_list)
        bucket_composition_dict[bucket] = stock_list
    print(bucket_composition_dict)
    return bucket_composition_dict


def get_bucket_stock_prices():
    """
    Take dictionary for bucket containing stocks, price them
    """
    buckets = get_bucket_stock_quantities()
    print(buckets)
    for bucketid in buckets:
        print(bucketid)
        stock_list = buckets[bucketid]
        for stock in stock_list:
            st = stock["stock"]
            stock["price"] = st.latest_quote()
            stock["total_value"] = stock["price"].value * stock["quantity"]
    return buckets


@login_required
def buy_bucket(request):
    """
    Display buy bucket, allow purchasing of bucket
    """
    if request.method == "GET":
        buckets = get_bucket_stock_prices()
        template = "trade.html"
        c = {'buckets': buckets}
        return render(request, template, c)
    elif request.method == "POST":
        prof = request.user.profile
        try:
            account = TradingAccount.objects.get(profile=prof)
            bucketid = request.POST.get("bucket")
            if bucketid is None:
                return HttpResponse("You must specify a bucket")
            bucket = InvestmentBucket.objects.get(pk=bucketid)
            new_trade = TradeBucket(account=account, bucket=bucket)
            new_trade.save()
            return HttpResponse("Trade complete.")
        except ObjectDoesNotExist:
            return HttpResponse("""Please create a trading account first at the
            <a href='/trade/account'> account creation page </a>""")
    else:
        return HttpResponse("Please don't sniff urls")
