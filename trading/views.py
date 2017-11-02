"""
Views for trading
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from stocks.models import InvestmentBucket
from trading.models import TradingAccount, TradeBucket
from authentication.views import get_balance_as_dic
from django.http import HttpResponse
from collections import defaultdict

@login_required
def create_account(request):
    """
    Create a trading account (only allows one trading account/user)
    """
    if request.method == "GET":
        prof = request.user.profile
        try:
            account = TradingAccount.objects.get(profile=prof)
            return HttpResponse("You already have an account.")
        except ObjectDoesNotExist:
            context = {}
            template = "create_trading_account.html"
            return render(request, template, context)
    elif request.method == "POST":
        prof = request.user.profile
        name = request.POST.get("account_name")
        account = TradingAccount(account_name=name, profile=prof)
        account.save()
        return HttpResponse("Account succesfully created.")
    else:
        return HttpResponse("Please don't sniff urls")


def get_bucket_stock_quantities(all_buckets):
    """
    Get a dictionary for each bucket containing tickers, quantities
    """
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
    return bucket_composition_dict


def get_bucket_stock_prices(all_buckets):
    """
    Take dictionary for bucket containing stocks, price them
    """
    buckets = get_bucket_stock_quantities(all_buckets)
    for bucketid in buckets:
        stock_list = buckets[bucketid]
        for stock in stock_list:
            single = stock["stock"]
            stock["price"] = single.latest_quote()
            stock["total_value"] = stock["price"].value * stock["quantity"]
    return buckets


def get_available_cash_as_num(request):
    """
    Get available cash for a user
    """
    total = get_balance_as_dic(request)[-1]["total"]
    if request.user.profile.trading_account is None:
        return total
    user_accounts = request.user.profile.trading_account.all()
    bucket_trades = user_accounts[0].buckettrades
    for trade in bucket_trades.all():
        bucket = trade.bucket
        value = bucket.get_quote(trade.timestamp)
        value *= trade.quantity
        total -= value
    return total

def get_available_buckets(request):
    """
    Get buckets for which user has > 0 quantity
    """
    user_accounts = request.user.profile.trading_account.all()
    bucket_trades = user_accounts[0].buckettrades
    avail_buckets = defaultdict(int)
    for trade in bucket_trades.all():
        avail_buckets[trade.bucket] += trade.quantity
    return dict((k, v) for k, v in avail_buckets.items() if v > 0)


@login_required
def buy_bucket(request):
    """
    Display buy bucket, allow purchasing of bucket
    """
    if request.method == "GET":
        buckets = get_bucket_stock_prices(InvestmentBucket.objects.all())
        template = "trade.html"
        context = {'buckets': buckets, 'verb':'Buy'}
        return render(request, template, context)
    elif request.method == "POST":
        prof = request.user.profile
        try:
            account = TradingAccount.objects.get(profile=prof)
            bucketid = request.POST.get("bucket")
            if bucketid is None:
                return HttpResponse("You must specify a bucket")
            bucket = InvestmentBucket.objects.get(pk=bucketid)
            if get_available_cash_as_num(request) > bucket.get_quote():
                new_trade = TradeBucket(account=account, quantity=1, bucket=bucket)
                new_trade.save()
                return HttpResponse("Trade complete.")
            else:
                return HttpResponse("Not enough cash")
        except ObjectDoesNotExist:
            return HttpResponse("""Please create a trading account first at the
            <a href='/trade/account'> account creation page </a>""")
    else:
        return HttpResponse("Please don't sniff urls")


@login_required
def sell_bucket(request):
    """
    Display sell bucket, allow purchasing of bucket
    """
    if request.method == "GET":
        buckets = get_available_buckets(request)
        buckets = get_bucket_stock_prices(buckets)
        template = "trade.html"
        context = {'buckets': buckets, 'verb': 'Sell'}
        return render(request, template, context)
    elif request.method == "POST":
        prof = request.user.profile
        account = TradingAccount.objects.get(profile=prof)
        bucketid = request.POST.get("bucket")
        if bucketid is None:
            return HttpResponse("You must specify a bucket")
        bucket = InvestmentBucket.objects.get(pk=bucketid)
        new_trade = TradeBucket(account=account, quantity=-1, bucket=bucket)
        new_trade.save()
        return HttpResponse("Trade complete.")
    else:
        return HttpResponse("Please don't sniff urls")


@login_required
def get_available_cash(request):
    """
    Display available cash as request
    """
    resp = get_available_cash_as_num(request)
    return HttpResponse(resp)
