"""
Views for authentication. Basically supports login/logout.
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
import plaid
from authentication.models import UserBank


PLAID_CLIENT_ID = '59c3248dbdc6a40ac87ed3e8'
PLAID_SECRET = 'ee7f10de9feb7d6408d1f5bd980f2a'
PLAID_PUBLIC_KEY = '2aa70186194f3a8d2038d989715a32'
PLAID_ENV = 'sandbox'


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
    return HttpResponseRedirect("/")


@login_required
def setup_bank(request):
    """
    Function to serve bank setup page
    """
    return render(request, "setup_bank.html", {})


@login_required
def get_access_token(request):
    """
    Function to retrieve plaid access token
    """
    if request.method == "POST":
        client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                              public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
        public_token = request.POST.get('public_token')
        exchange_response = client.Item.public_token.exchange(public_token)
        plaidrequest = client.Item.get(exchange_response['access_token'])
        bank_user = UserBank(
            user=request.user,
            item_id=exchange_response['item_id'],
            access_token=exchange_response['access_token'],
            institution_name=plaidrequest['item']['institution_id'],
            )
        bank_user.save()
        request.user.profile.has_bank_linked = True
        request.user.save()
        return HttpResponseRedirect("/home")
    return HttpResponse("Please don't sniff urls")


@login_required
def list_transactions(request):
    """
    A demo view to list all of a user's transactions
    """
    if request.method == "POST":
        user_bank_id = request.POST.get('id')
        user_bank = UserBank.objects.get(pk=user_bank_id)
        if user_bank.user == request.user:
            client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
            response = client.Transactions.get(user_bank.access_token,
                                               start_date='2016-07-12', end_date='2017-01-09')
            transactions = response['transactions']
            context = {'tx': transactions}
            return render(request, "list_transactions.html", context)
        return HttpResponse("You don't have permission to view that.")
    userbank = request.user.userbank_set.all()
    context = {'userbank': userbank}
    return render(request, 'bank_select_form.html', context)
