"""
Plaid setup
"""
import os
from django.utils.deprecation import MiddlewareMixin
import plaid

PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')
PLAID_ENV = 'sandbox' if os.environ.get('DEBUG') == "TRUE" else 'development'


# pylint: disable=too-few-public-methods
class PlaidMiddleware(MiddlewareMixin):
    """
    Simple Middleware to inject plaid client into request object
    """
    def __init__(self, get_response):
        super(PlaidMiddleware, self).__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        print("Enter")
        request.plaid = plaid.Client(
            client_id=PLAID_CLIENT_ID,
            secret=PLAID_SECRET,
            public_key=PLAID_PUBLIC_KEY,
            environment=PLAID_ENV
        )
        response = self.get_response(request)
        return response
# pylint: enable=too-few-public-methods
