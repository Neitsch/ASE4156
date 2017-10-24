"""
Views for authentication. Basically supports login/logout.
"""
import datetime
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
import plaid
from authentication.models import UserBank


PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')
PLAID_ENV = 'sandbox' if os.environ.get('DEBUG') == "TRUE" else 'development'


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
    if not request.user.profile.has_bank_linked:
        return render(request, "setup_bank.html", {})
    return HttpResponseRedirect('/home')


@login_required
def get_access_token(request):
    """
    Function to retrieve plaid access token
    """
    if request.method == "POST":
        client = request.plaid
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
        return HttpResponse(status=201)
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
            start = datetime.datetime.now() - datetime.timedelta(days=365)
            start = start.strftime("%Y-%m-%d")
            end = datetime.datetime.now().strftime("%Y-%m-%d")
            response = client.Transactions.get(user_bank.access_token,
                                               start_date=start, end_date=end)
            transactions = response['transactions']
            context = {'tx': transactions}
            return render(request, "list_transactions.html", context)
        return HttpResponse("You don't have permission to view that.")
    userbank = request.user.userbank_set.all()
    context = {'userbank': userbank}
    return render(request, 'bank_select_form.html', context)


@login_required
def get_balance(request):
    """
    A view that gets all balances for a user and returns as json
    """
    client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                          public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
    for user_bank in request.user.userbank_set.all():
        if user_bank.user == request.user:
            response = client.Accounts.balance.get(user_bank.access_token)
            json_response = []
            for account in response['accounts']:
                dic = {}
                dic['name'] = account['official_name']
                if account['subtype'] == 'cd':
                    dic['balance'] = account['balances']['current']
                elif account['subtype'] == 'credit card':
                    dic['balance'] = int("-{}".format(account['balances']['current']))
                else:
                    dic['balance'] = account['balances']['available']
                dic['type'] = account['subtype']
                json_response.append(dic)
            return JsonResponse(json_response, safe=False)
        return HttpResponse("You don't have permission to view that.")
    return HttpResponse("No user signed in/bank selected")
