from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import City, Taluka, District, State, Pradesh, BhagatDetail
import json
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Create your views here.
@login_required(login_url="/login")
def cityAdd(request):
    if request.method == "POST":
        cityName = request.POST["cityName"]
        state = request.POST["state"]
        district = request.POST["district"]
        taluka = request.POST["taluka"]
        pincode = request.POST["pincode"]
        pradesh = request.POST["pradesh"]
        cityInstance = City()
        cityInstance.cityName = cityName
        cityInstance.pincode = pincode
        cityInstance.state = State.objects.filter(
            district=District.objects.filter(districtName=district).first()
        ).first()
        cityInstance.district = District.objects.filter(districtName=district).first()
        cityInstance.taluka = Taluka.objects.filter(talukaName=taluka).first()
        cityInstance.pradesh = Pradesh.objects.filter(pradeshName=pradesh).first()
        cityInstance.save()
        return redirect("/location")
    else:
        if request.session.has_key("username"):
            user = request.user
            states = State.objects.all()
            stateArr = []
            for state in states:
                stateArr.append(state.stateName)
            pradeshs = Pradesh.objects.all()
            pradeshArr = []
            for pradesh in pradeshs:
                pradeshArr.append(pradesh.pradeshName)
            return render(
                request,
                "cityAdd.html",
                {
                    "user": user,
                    "stateArr": stateArr,
                    "pradeshArr": pradeshArr,
                    "user": user,
                    "sessionTime": request.session["sessionStartTime"],
                    "site_key": settings.RECAPTCHA_SITE_KEY,
                    "sessionEnd": int(request.session.get_expiry_age() / 100),
                    "error": "",
                    "msg": "",
                },
            )
        else:
            return redirect("/login")
