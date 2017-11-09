"""
Views for authentication. Basically supports login/logout.
"""
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
import plaid
from authentication.models import UserBank


PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')
PLAID_ENV = (
    'sandbox'
    if os.environ.get('DEBUG') == "TRUE"
    or os.environ.get('TRAVIS_BRANCH') is not None
    else 'development')

def login(request):
    """
    Dummy function to render login page
    """
    return render(request, 'auth.html')


def logout(request):
    """
    Function to logout
    """

    log_out(request)
    return HttpResponseRedirect("/login")


@login_required
def setup_bank(request):
    """
    Function to serve bank setup page
    """
    if not request.user.profile.has_bank_linked:
        return render(request, "setup_bank.html", {})
    return HttpResponseRedirect('/home')


@login_required
def get_access_token(request):
    """
    Function to retrieve plaid access token
    """
    if request.method == "POST":
        client = plaid.Client(
            client_id=PLAID_CLIENT_ID,
            secret=PLAID_SECRET,
            public_key=PLAID_PUBLIC_KEY,
            environment=PLAID_ENV
        )
        public_token = request.POST.get('public_token')
        exchange_response = client.Item.public_token.exchange(public_token)
        plaidrequest = client.Item.get(exchange_response['access_token'])
        bank_user = UserBank(
            user=request.user,
            item_id=exchange_response['item_id'],
            access_token=exchange_response['access_token'],
            institution_name=plaidrequest['item']['institution_id'],
        )
        bank_user.current_balance_field = bank_user.plaid().current_balance()
        bank_user.account_name_field = bank_user.plaid().account_name()
        bank_user.income_field = bank_user.plaid().income()
        bank_user.expenditure_field = bank_user.plaid().expenditure()
        bank_user.save()
        request.user.profile.has_bank_linked = True
        request.user.save()
        return HttpResponse(status=201)
    return HttpResponse("Please don't sniff urls")
