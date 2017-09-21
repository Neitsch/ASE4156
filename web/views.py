from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


@login_required
def home(request):
    if request.user.profile.has_bank_linked is not True:
        return HttpResponseRedirect('/setup_bank')
    else:
        return render(request, "home.html", {})
