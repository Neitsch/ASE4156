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
		u = UserBank(
			user=request.user,
			item_id=exchange_response['item_id'],
			access_token=exchange_response['access_token']
			)
		u.save()
		request.user.profile.has_bank_linked = True
		request.user.save()
		return HttpResponseRedirect("/home")
	return HttpResponse("Please don't sniff urls")
