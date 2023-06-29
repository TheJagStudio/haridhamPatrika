from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import City, Taluka, District, State, Pradesh, BhagatDetail, Zone
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
import string
import random
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import base64
from io import BytesIO

districtArr = {"ADD": "Ahmedabad",
               "AL": "Amreli",
               "AND": "Anand",
               "SK": "Banaskantha",
               "BC": "Bharuch",
               "BHR": "Bhavnagar",
               "PL": "Dahod",
               "DG": "Dangs",
               "GRD": "Gandhinagar",
               "JR": "Jamnagar",
               "JD": "Junagadh",
               "BHK": "Kutchh",
               "KD": "Kheda",
               "MN": "Mahesana",
               "NRM": "Narmada",
               "NV": "Navsari",
               "MN": "Patan",
               "PL": "Panchmahal",
               "JD": "Porbandar",
               "RTD": "Rajkot",
               "SK": "Sabarkantha",
               "SR": "Surendranagar",
               "STD": "Surat",
               "TP": "Tapi",
               "VRD": "Vadodara",
               "VD": "Valsad",
               "BY": "Mumbai",
               "NI": "Sirohi",
               "NI": "Bhadohi",
               "SI": "Chennai",
               "VD": "Daman",
               "NI": "Delhi",
               "BY": "Thane",
               "BY": "Navi Mumbai",
               "SI": "Hyderabad",
               "JD": "Gir-Somnath",
               "NI": "Durg C. G.",
               "NI": "Bilaspur",
               "SI": "Aurangabad",
               "NI": "Moga",
               "BY": "Raigad",
               "SI": "Pune",
               "SI": "Jalgaon",
               "SI": "Bangalore",
               "NI": "Varanasi",
               "MP": "Bhopal",
               "VD": "Dadra Nagar Haveli",
               "MP": "Hoshangabad",
               "MP": "Indore",
               "NI": "Jaipur",
               "NI": "Jalandhar",
               "NI": "Kota",
               "NI": "Lucknow",
               "NI": "Ludhiana",
               "SI": "Nagpur",
               "MP": "Ratlam",
               "NI": "Jaunpur",
               "SI": "Tiruchirappalli",
               "MP": "Ujjain",
               "SI": "Yavatmal",
               "SI": "Solapur",
               "NI": "Mohali",
               "NI": "Agra",
               "NI": "Udaipur",
               "MP": "Jhabua",
               "NI": "Pali",
               "SI": "Wardha",
               "NI": "Faridabad",
               "SI": "Dhule",
               "NI": "Bulandshahr",
               "NI": "Hardoi",
               "SK": "Aravalli",
               "BHR": "Botad",
               "VRD": "Chhota Udaipur",
               "KD": "Mahisagar",
               "RTD": "Morbi",
               "JR": "Devbhumi-Dwarka",
               "SI": "Adilabad",
               "NI": "Una",
               "SI": "Palghar",
               "NI": "Gondia",
               "MP": "Alirajpur",
               "NI": "New Delhi",
               "SI": "Mysore",
               "LA": "Swikrut",
               "NI": "Raipur",
               "NI": "Kanagra",
               "NI": "Solan",
               "SI": "Warangal",
               "NI": "Kanpur",
               "MP": "Dewas",
               "NI": "Azamgarh",
               "SI": "Kalaburgi"}


def gCaptchaVerifer(token):
    secret_key = settings.RECAPTCHA_SECRET_KEY
    data = {
        'response': token,
        'secret': secret_key
    }
    resp = requests.post(
        'https://www.google.com/recaptcha/api/siteverify', data=data)
    return resp.json()


@login_required(login_url='/login')
def home(request):
    #for data in BhagatDetail.objects.all():
    #    print(data.name)
    #    data.qrcode = data.qrcode[2:-1]
    #    data.save()
    #
    if request.session.has_key('username'):
        user = request.user
        with open("./static/data.json", "r") as f:
            data = json.loads(f.read())
        dataFinal = random.choice(data["data"])
        embedLink = "https://www.youtube.com/embed/" + \
            dataFinal["link"].split("v=")[1]
        return render(request, "index.html", {"embedLink": embedLink, "user": user,"sessionTime": request.session['sessionStartTime'], 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
    else:
        return redirect("/login")


@login_required(login_url='/login')
def userAdd(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
            if not result_json.get('success'):
                response = render(request, "404.html")
                response.status_code = 404
                return response
            else:
                try:
                    receiptNo = request.POST["receiptNo"]
                    receiptDate = request.POST["receiptDate"]
                    subYear = request.POST["subYear"]
                    endDate = request.POST["endDate"]
                    name = request.POST["name"]
                    email = request.POST["email"]
                    phone = request.POST["phone"]
                    address1 = request.POST["address1"]
                    address2 = request.POST["address2"]
                    address3 = request.POST["address3"]
                    state = request.POST["state"]
                    district = request.POST["district"]
                    taluka = request.POST["taluka"]
                    city = request.POST["city"]
                    pincode = request.POST["pincode"]
                    is_zone = request.POST.get("is_zone",False)
                    print(is_zone)
                    if is_zone == "true":
                        is_zone = True
                        #zone = request.POST["zone"]
                        pass
                    remark = request.POST["remark"]
                    entryDate = str(date.today())
                    dataid = str(''.join(random.choices(
                        string.ascii_uppercase, k=6)))
                    while BhagatDetail.objects.filter(dataid=dataid).count() > 0:
                        dataid = str(''.join(random.choices(
                            string.ascii_uppercase, k=6)))
                    entryInstance = BhagatDetail()
                    entryInstance.districtCode = District.objects.filter(
                        districtName=district).first().districtCode
                    entryInstance.dataid = dataid
                    entryInstance.receiptNo = receiptNo
                    entryInstance.entryDate = entryDate
                    entryInstance.startDate = receiptDate.split("-")[2]+"-"+receiptDate.split("-")[1]+"-"+receiptDate.split("-")[0]
                    entryInstance.endDate = endDate.split("-")[2]+"-"+endDate.split("-")[1]+"-"+endDate.split("-")[0]
                    entryInstance.subYear = subYear
                    entryInstance.name = name
                    entryInstance.email = email
                    entryInstance.addressOne = address1
                    entryInstance.addressTwo = address2
                    entryInstance.addressThree = address3
                    entryInstance.state = State.objects.filter(
                        stateName=state).first()
                    entryInstance.district = District.objects.filter(
                        districtName=district, state=entryInstance.state).first()
                    entryInstance.taluka = Taluka.objects.filter(
                        talukaName=taluka, district=entryInstance.district).first()
                    entryInstance.city = City.objects.filter(
                        cityName=city, taluka=entryInstance.taluka).first()
                    entryInstance.pradesh = entryInstance.city.pradesh
                    entryInstance.newFlag = True
                    entryInstance.dontSendFlag = False
                    entryInstance.is_active = True
                    entryInstance.phoneNum = phone
                    entryInstance.pincode = pincode
                    entryInstance.remark = remark
                    entryInstance.is_zone = is_zone
                    entryInstance.save()
                    # Tracker.objects.create_from_request(request, entryInstance)
                    msg = "Successfully added a new Entry in database."
                    error = ""
                except Exception as e:
                    msg = ""
                    error = e
                states = State.objects.all()
                stateArr = []
                for state in states:
                    stateArr.append(state.stateName)
                return render(request, "userAdd.html", {"user": request.user, "stateArr": stateArr, "msg": msg, "error": error, "sessionTime": request.session['sessionStartTime'], 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
        else:
            user = request.user
            states = State.objects.all()
            stateArr = []
            for state in states:
                stateArr.append(state.stateName)
            return render(request, "userAdd.html", {"user": user, "stateArr": stateArr, "msg": "", "error": "", "sessionTime": request.session['sessionStartTime'], 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
    else:
        return redirect("/login")


@login_required(login_url='/login')
def userEdit(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
            if not result_json.get('success'):
                response = render(request, "404.html")
                response.status_code = 404
                return response
            else:
                try:
                    receiptNo = request.POST.get("receiptNo", "").strip()
                    receiptDate = request.POST.get("receiptDate", "").strip()
                    subYear = request.POST.get("subYear", "").strip()
                    endDate = request.POST.get("endDate", "").strip()
                    name = request.POST.get("name", "").strip()
                    email = request.POST.get("email", "").strip()
                    phone = request.POST.get("phone", "").strip()
                    address1 = request.POST.get("address1", "").strip()
                    address2 = request.POST.get("address2", "").strip()
                    address3 = request.POST.get("address3", "").strip()
                    state = request.POST.get("state", "").strip()
                    district = request.POST.get("district", "").strip()
                    taluka = request.POST.get("taluka", "").strip()
                    city = request.POST.get("city", "").strip()
                    pincode = request.POST.get("pincode", "").strip()
                    # is_zone = request.POST["is_zone"]
                    # if is_zone == "true":
                    #    zone = request.POST["zone"]
                    remark = request.POST.get("remark", "").strip()
                    entryDate = str(date.today())
                    print(entryDate)
                    entryInstance = BhagatDetail.objects.filter(
                        receiptNo=receiptNo.strip()).first()
                    entryInstance.districtCode = District.objects.filter(
                        districtName=district).first().districtCode
                    entryInstance.receiptNo = receiptNo
                    entryInstance.entryDate = entryDate
                    entryInstance.startDate = receiptDate.split("-")[2]+"-"+receiptDate.split("-")[1]+"-"+receiptDate.split("-")[0]
                    entryInstance.endDate = endDate.split("-")[2]+"-"+endDate.split("-")[1]+"-"+endDate.split("-")[0]
                    entryInstance.subYear = int(
                        subYear) if subYear != "" else entryInstance.subYear
                    entryInstance.name = name
                    entryInstance.email = email
                    entryInstance.addressOne = address1
                    entryInstance.addressTwo = address2
                    entryInstance.addressThree = address3
                    entryInstance.state = State.objects.filter(
                        stateName=state).first()
                    entryInstance.district = District.objects.filter(
                        districtName=district, state=entryInstance.state).first()
                    entryInstance.taluka = Taluka.objects.filter(
                        talukaName=taluka, district=entryInstance.district).first()
                    entryInstance.city = City.objects.filter(
                        cityName=city, taluka=entryInstance.taluka).first()
                    entryInstance.pradesh = entryInstance.city.pradesh
                    entryInstance.phoneNum = phone
                    entryInstance.pincode = pincode
                    entryInstance.remark = remark
                    entryInstance.save()
                    msg = "Successfully edited a Entry in database."
                    error = ""
                except Exception as e:
                    msg = ""
                    error = e
                states = State.objects.all()
                stateArr = []
                for state in states:
                    stateArr.append(state.stateName)
                return render(request, "userEdit.html", {"user": request.user, "stateArr": stateArr, "msg": msg, "error": error, "sessionTime": request.session['sessionStartTime'], 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
        else:
            msg = ""
            error = ""
            user = request.user
            states = State.objects.all()
            stateArr = []
            for state in states:
                stateArr.append(state.stateName)
            return render(request, "userEdit.html", {"user": user, "stateArr": stateArr, "msg": "", "error": "", "sessionTime": request.session['sessionStartTime'], 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
    else:
        return redirect("/login")


@login_required(login_url='/login')
def userList(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
            if not result_json.get('success'):
                response = render(request, "404.html")
                response.status_code = 404
                return response
            else:
                try:
                    msg = "Successfully edited a Entry in database."
                    error = ""
                except Exception as e:
                    msg = ""
                    error = e
                states = State.objects.all()
                stateArr = []
                for state in states:
                    stateArr.append(state.stateName)
                return render(request, "userList.html", {"user": request.user, "stateArr": stateArr, "msg": msg, "error": error, "sessionTime": request.session['sessionStartTime'], 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
        else:
            msg = ""
            error = ""
            user = request.user
            states = State.objects.all()
            stateArr = []
            for state in states:
                stateArr.append(state.stateName)
            return render(request, "userList.html", {"user": user, "stateArr": stateArr, "msg": "", "error": "", "sessionTime": request.session['sessionStartTime'], 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
    else:
        return redirect("/login")


def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            remember = request.POST['rememberMe']
        except:
            remember = "False"
        next = request.POST['next']
        if next == '':
            next = '/'
        result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
        if not result_json.get('success'):
            response = render(request, "404.html")
            response.status_code = 404
            return response
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if remember == "False":
                    request.session.set_expiry(1500)
                else:
                    request.session.set_expiry(144000)
                now = datetime.now(timezone("Asia/Kolkata"))
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                request.session['sessionStartTime'] = dt_string
                request.session['username'] = username
                return redirect(next)
            else:
                return render(request, "login.html", {"error": "Invalid username or password", 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})
    else:
        return render(request, "login.html", {"error": "", 'site_key': settings.RECAPTCHA_SITE_KEY,"sessionEnd":int(request.session.get_expiry_age()/100)})


@login_required(login_url='/login')
def logoutPage(request):
    try:
        del request.session['username']
        del request.session['sessionStartTime']
    except:
        pass
    try:
        next = request.GET['next']
        print(next)
    except:
            next = '/'
    logout(request)
    return redirect("/login?next="+next)


def profile(request, dataid):
    if len(dataid) == 6:
        entryData = BhagatDetail.objects.filter(dataid=dataid).first()
        if entryData is not None:
            states = State.objects.all()
            stateArr = []
            for state in states:
                stateArr.append(state.stateName)
            context = {
                "stateArr":stateArr,
                "districtCode": entryData.districtCode,
                "dataid": entryData.dataid,
                "entryDate": entryData.entryDate,
                "startDate": entryData.startDate,
                "endDate": entryData.endDate,
                "subYear": entryData.subYear,
                "name": entryData.name,
                "addressOne": entryData.addressOne,
                "addressTwo": entryData.addressTwo,
                "addressThree": entryData.addressThree,
                "city": entryData.city.cityName,
                "taluka": entryData.taluka.talukaName,
                "district": entryData.district.districtName,
                "state": entryData.state.stateName,
                "phoneNum": entryData.phoneNum,
                'site_key': settings.RECAPTCHA_SITE_KEY,
                "sessionEnd":int(request.session.get_expiry_age()/100)
            }
            return render(request, "profile.html", context)
        else:
            response = render(request, "404.html")
            response.status_code = 404
            return response
    else:
        response = render(request, "404.html")
        response.status_code = 404
        return response
