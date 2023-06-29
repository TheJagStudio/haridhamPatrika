from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import City, Taluka, District, State, Pradesh, BhagatDetail
import json
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import string
from datetime import date
from datetime import datetime
from pytz import timezone
import csv
import pandas as pd
from django.conf import settings
import requests


@login_required(login_url='/login')
def allList(request):
    if request.session.has_key('username'):
        user = request.user
        msg = ""
        error = ""
        return render(request, "allList.html", {"user": user, 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100), "msg": msg, "error": error, "sessionTime": request.session['sessionStartTime']})
    else:
        return redirect("/login")
