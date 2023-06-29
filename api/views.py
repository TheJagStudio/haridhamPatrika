from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import City, Taluka, District, State, Pradesh, BhagatDetail
import json
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import razorpay
from main.views import gCaptchaVerifer
from django.conf import settings
import math
from django.template.loader import get_template
from dateutil import parser
from datetime import date,datetime,timedelta
import pdfkit
from os import listdir
from os.path import isfile, join
import zipfile

config = pdfkit.configuration(wkhtmltopdf=r'D:\patrika\patrika\wkhtmltopdf\bin\wkhtmltopdf.exe')
options = {
    'page-size': 'A4',
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
    'encoding': "UTF-8",
    'no-outline': None
}

client = razorpay.Client(
    auth=("rzp_test_EdIMHRHA7suoML", "RBJc7ZCTLEBky3n2To6UyufG"))


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    with open("./labels/html/"+context_dict["code"]+".html","w") as f:
        f.write(html)
    return HttpResponse(html)

# Create your views here.


@login_required(login_url='/login')
def details(request):
    if request.session.has_key('username'):
        return HttpResponse("Hello moto")
    else:
        return redirect("/login")


@login_required(login_url='/login')
def districtFinder(request):
    if request.method == 'POST':
        result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
        if not result_json.get('success'):
            response = render(request, "404.html")
            response.status_code = 404
            return response
        else:
            state = request.POST['state']
            districts = District.objects.filter(
                state=State.objects.filter(stateName=state).first()).all()
            districtArr = []
            for district in districts:
                districtArr.append(district.districtName)
            return HttpResponse(json.dumps({"data": districtArr}), content_type="application/json")
    else:
        return redirect("/login")


@login_required(login_url='/login')
def talukaFinder(request):
    if request.method == 'POST':
        result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
        if not result_json.get('success'):
            response = render(request, "404.html")
            response.status_code = 404
            return response
        else:
            district = request.POST['district']
            talukas = Taluka.objects.filter(
                district=District.objects.filter(districtName=district).first()).all()
            talukaArr = []
            for taluka in talukas:
                talukaArr.append(taluka.talukaName)
            return HttpResponse(json.dumps({"data": talukaArr}), content_type="application/json")
    else:
        return redirect("/login")


@login_required(login_url='/login')
def cityFinder(request):
    if request.method == 'POST':
        result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
        if not result_json.get('success'):
            response = render(request, "404.html")
            response.status_code = 404
            return response
        else:
            district = request.POST['district']
            taluka = request.POST['taluka']
            citys = City.objects.filter(district=District.objects.filter(districtName=district).first(
            ), taluka=Taluka.objects.filter(talukaName=taluka).first()).all()
            citysArr = []
            for city in citys:
                citysArr.append(city.cityName)
            return HttpResponse(json.dumps({"data": citysArr}), content_type="application/json")
    else:
        return redirect("/login")


@login_required(login_url='/login')
def entryFinder(request):
    if request.method == 'POST':
        result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
        if not result_json.get('success'):
            response = render(request, "404.html")
            response.status_code = 404
            return response
        else:
            try:
                dataType = request.POST['dataType']
                dataValue = request.POST['dataValue']
                if dataType == 'receiptNo':
                    entry = BhagatDetail.objects.filter(
                        receiptNo=dataValue.strip()).first()
                    print(entry)
                else:
                    entry = BhagatDetail.objects.filter(
                        id=dataValue.strip()).first()
                dt = parser.parse(str(entry.endDate))
                entry.endDate = str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                dt = parser.parse(str(entry.startDate))
                entry.startDate = str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)
                entryData = [entry.startDate, entry.subYear, entry.endDate, entry.name, entry.email, entry.phoneNum, entry.addressOne, entry.addressTwo,
                             entry.addressThree, entry.city.cityName, entry.taluka.talukaName, entry.district.districtName, entry.state.stateName, entry.pincode, entry.remark]
                return HttpResponse(json.dumps({"data": entryData}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({"data": "error"}), content_type="application/json")
    else:
        return redirect("/login")

def profileEdit(request):
    pass

@login_required(login_url='/login')
def listFinder(request):
    if request.method == 'POST':
        result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
        if not result_json.get('success'):
            response = render(request, "404.html")
            response.status_code = 404
            return response
        else:
            try:
                code = request.POST['code']
                entryData = []
                if code == "ADD":
                    cityAhemdabad = City.objects.filter(
                        cityName="Ahmedabad").first()
                    dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
                        city=cityAhemdabad).exclude(is_active=False).order_by('name').values())
                elif code == "RTD":
                    cityRajkot = City.objects.filter(cityName="Rajkot").first()
                    dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
                        city=cityRajkot).exclude(is_active=False).order_by('name').values())
                elif code == "VRD":
                    cityVadodara = City.objects.filter(
                        cityName="Vadodara").first()
                    talukaPadra = Taluka.objects.filter(
                        talukaName="Padra").first()
                    dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
                        city=cityVadodara).exclude(is_active=False).exclude(taluka=talukaPadra).order_by('name').values())
                elif code == "VD":
                    cityVadodara = City.objects.filter(
                        cityName="Vadodara").first()
                    dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
                        city=cityVadodara).exclude(is_active=False).order_by('name').values())
                elif code == "BC":
                    cityBharuch = City.objects.filter(
                        cityName="Bharuch").first()
                    cityZadeshwar = City.objects.filter(
                        cityName="Zadeshwar").first()
                    talukaJambusar = Taluka.objects.filter(
                        talukaName="Jambusar").first()
                    dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(city=cityBharuch).exclude(
                        city=cityZadeshwar).exclude(is_active=False).exclude(taluka=talukaJambusar).order_by('name').values())
                elif code == "Amadavad":
                    cityAhmedabad = City.objects.filter(
                        cityName="Ahmedabad").first()
                    dataList = list(BhagatDetail.objects.filter(
                        city=cityAhmedabad).exclude(is_active=False).order_by('name').values())
                elif code == "Rajkot":
                    cityRajkot = City.objects.filter(cityName="Rajkot").first()
                    dataList = list(BhagatDetail.objects.filter(
                        city=cityRajkot).exclude(is_active=False).order_by('name').values())
                elif code == "Vadodara":
                    cityVadodara = City.objects.filter(
                        cityName="Vadodara").first()
                    dataList = list(BhagatDetail.objects.filter(
                        city=cityVadodara).exclude(is_active=False).order_by('name').values())
                elif code == "Surat":
                    citySurat = City.objects.filter(cityName="Surat").first()
                    dataList = list(BhagatDetail.objects.filter(
                        city=citySurat).exclude(is_active=False).order_by('name').values())
                elif code == "Bharuch":
                    cityBharuch = City.objects.filter(
                        cityName="Bharuch").first()
                    dataList = list(BhagatDetail.objects.filter(
                        city=cityBharuch).exclude(is_active=False).order_by('name').values())
                    cityBharuch = City.objects.filter(
                        cityName="Zadeshwar").first()
                    for tempData in list((BhagatDetail.objects.filter(city=cityBharuch).exclude(is_active=False).order_by('name').values())):
                        dataList.append(tempData)
                elif code == "Jambusar":
                    talukaJambusar = Taluka.objects.filter(
                        talukaName="Jambusar").first()
                    dataList = list(BhagatDetail.objects.filter(
                        taluka=talukaJambusar).exclude(is_active=False).order_by('name').values())
                elif code == "Padra":
                    cityPadra = City.objects.filter(cityName="Padra").first()
                    dataList = list(BhagatDetail.objects.filter(
                        city=cityPadra).exclude(is_active=False).order_by('name').values())
                elif code == "Navi Pradi":
                    districtSurat = District.objects.filter(
                        districtName="Surat").first()
                    citySurat = City.objects.filter(cityName="Surat").first()
                    dataList = list(BhagatDetail.objects.filter(district=districtSurat).exclude(
                        city=citySurat).exclude(is_active=False).order_by('name').values())
                else:
                    dataList = list(BhagatDetail.objects.filter(
                        districtCode=code).exclude(is_active=False).order_by('name').values())
                count = 1
                cityId = ""
                talukaId = ""
                districtId = ""
                stateId = ""
                try:
                    city = City.objects.filter(id=int(cityId)).first().cityName
                except:
                    city = ""
                try:
                    taluka = Taluka.objects.filter(
                        id=int(talukaId)).first().talukaName
                except:
                    taluka = ""
                try:
                    district = District.objects.filter(
                        id=int(districtId)).first().districtName
                except:
                    district = ""
                try:
                    state = State.objects.filter(
                        id=int(stateId)).first().stateName
                except:
                    state = ""
                for data in dataList:
                    if cityId != data['city_id'] or talukaId != data['taluka_id'] or districtId != data['district_id'] or stateId != data['state_id']:
                        cityId = data['city_id']
                        talukaId = data['taluka_id']
                        districtId = data['district_id']
                        stateId = data['state_id']
                        try:
                            city = City.objects.filter(
                                id=int(cityId)).first().cityName
                        except:
                            city = ""
                        try:
                            taluka = Taluka.objects.filter(
                                id=int(talukaId)).first().talukaName
                        except:
                            taluka = ""
                        try:
                            district = District.objects.filter(
                                id=int(districtId)).first().districtName
                        except:
                            district = ""
                        try:
                            state = State.objects.filter(
                                id=int(stateId)).first().stateName
                        except:
                            state = ""
                    dt = parser.parse(str(data['startDate']))
                    data['startDate'] = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
                    dt = parser.parse(str(data['endDate']))
                    data['endDate'] = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
                    entryData.append([count, data['districtCode'], data['receiptNo'], data['startDate'], data['subYear'], data['endDate'], data['name'], data['addressOne'],
                                     data['addressTwo'], data['addressThree'], city, taluka, district, state, data['phoneNum'], data['pincode'], data['email'], data['remark'], data['dataid']])
                    count = count + 1
                return HttpResponse(json.dumps({"data": entryData}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({"data": str(e)}), content_type="application/json")
    else:
        return redirect("/login")


def listFinderLocal(code):
    entryData = []
    if code == "ADD":
        cityAhemdabad = City.objects.filter(cityName="Ahmedabad").first()
        dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
            city=cityAhemdabad).exclude(is_active=False).order_by('name').values())
    elif code == "RTD":
        cityRajkot = City.objects.filter(cityName="Rajkot").first()
        dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
            city=cityRajkot).exclude(is_active=False).order_by('name').values())
    elif code == "VRD":
        cityVadodara = City.objects.filter(cityName="Vadodara").first()
        talukaPadra = Taluka.objects.filter(talukaName="Padra").first()
        dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
            city=cityVadodara).exclude(is_active=False).exclude(taluka=talukaPadra).order_by('name').values())
    elif code == "VD":
        cityVadodara = City.objects.filter(cityName="Vadodara").first()
        dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(
            city=cityVadodara).exclude(is_active=False).order_by('name').values())
    elif code == "BC":
        cityBharuch = City.objects.filter(cityName="Bharuch").first()
        cityZadeshwar = City.objects.filter(cityName="Zadeshwar").first()
        talukaJambusar = Taluka.objects.filter(talukaName="Jambusar").first()
        dataList = list(BhagatDetail.objects.filter(districtCode=code).exclude(city=cityBharuch).exclude(
            city=cityZadeshwar).exclude(is_active=False).exclude(taluka=talukaJambusar).order_by('name').values())
    elif code == "Amadavad":
        cityAhmedabad = City.objects.filter(cityName="Ahmedabad").first()
        dataList = list(BhagatDetail.objects.filter(
            city=cityAhmedabad).exclude(is_active=False).order_by('name').values())
    elif code == "Rajkot":
        cityRajkot = City.objects.filter(cityName="Rajkot").first()
        dataList = list(BhagatDetail.objects.filter(
            city=cityRajkot).exclude(is_active=False).order_by('name').values())
    elif code == "Vadodara":
        cityVadodara = City.objects.filter(cityName="Vadodara").first()
        dataList = list(BhagatDetail.objects.filter(
            city=cityVadodara).exclude(is_active=False).order_by('name').values())
    elif code == "Surat":
        citySurat = City.objects.filter(cityName="Surat").first()
        dataList = list(BhagatDetail.objects.filter(
            city=citySurat).exclude(is_active=False).order_by('name').values())
    elif code == "Bharuch":
        cityBharuch = City.objects.filter(cityName="Bharuch").first()
        dataList = list(BhagatDetail.objects.filter(
            city=cityBharuch).exclude(is_active=False).order_by('name').values())
        cityBharuch = City.objects.filter(cityName="Zadeshwar").first()
        for tempData in list((BhagatDetail.objects.filter(city=cityBharuch).exclude(is_active=False).order_by('name').values())):
            dataList.append(tempData)
    elif code == "Jambusar":
        talukaJambusar = Taluka.objects.filter(talukaName="Jambusar").first()
        dataList = list(BhagatDetail.objects.filter(
            taluka=talukaJambusar).exclude(is_active=False).order_by('name').values())
    elif code == "Padra":
        cityPadra = City.objects.filter(cityName="Padra").first()
        dataList = list(BhagatDetail.objects.filter(
            city=cityPadra).exclude(is_active=False).order_by('name').values())
    elif code == "Navi Pradi":
        districtSurat = District.objects.filter(districtName="Surat").first()
        citySurat = City.objects.filter(cityName="Surat").first()
        dataList = list(BhagatDetail.objects.filter(district=districtSurat).exclude(
            city=citySurat).exclude(is_active=False).order_by('name').values())
    else:
        dataList = list(BhagatDetail.objects.filter(
            districtCode=code).exclude(is_active=False).order_by('name').values())
    count = 1
    cityId = ""
    talukaId = ""
    districtId = ""
    stateId = ""
    try:
        city = City.objects.filter(id=int(cityId)).first().cityName
    except:
        city = ""
    try:
        taluka = Taluka.objects.filter(id=int(talukaId)).first().talukaName
    except:
        taluka = ""
    try:
        district = District.objects.filter(
            id=int(districtId)).first().districtName
    except:
        district = ""
    for data in dataList:
        if cityId != data['city_id'] or talukaId != data['taluka_id'] or districtId != data['district_id'] or stateId != data['state_id']:
            cityId = data['city_id']
            talukaId = data['taluka_id']
            districtId = data['district_id']
            stateId = data['state_id']
            try:
                city = City.objects.filter(id=int(cityId)).first().cityName
            except:
                city = ""
            try:
                taluka = Taluka.objects.filter(
                    id=int(talukaId)).first().talukaName
            except:
                taluka = ""
            try:
                district = District.objects.filter(
                    id=int(districtId)).first().districtName
            except:
                district = ""
        dt = parser.parse(str(data['endDate']))
        expire = "False"
        if (datetime.now() - timedelta(days=60))>dt:
            expire = "True"
        if data['qrcode'] != "":
            img_str = data['qrcode']
        else:
            img_str = ""
        data['endDate'] = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
        entryData.append([data['districtCode'], data['disCount'],data['endDate'], data['name'], data['addressOne'],
                         data['addressTwo'], data['addressThree'],city,data['pincode'],taluka, district,data['qrcode'],expire,img_str])
        count = count + 1
    return entryData


@login_required(login_url='/login')
def labelExporter(request):
    codeArr = ['ADD', 'AL', 'AND', 'BC', 'BHK','BHR','DG','GRD','JD','JR','KD','MN','NRM','NV','PL','RTD','SK','SR','STD','TP','VD','VRD','Amadavad','Rajkot','Vadodara','BY','MP','NI','SI','Surat','Bharuch','Jambusar','Padra','Navi Pradi']
    for code in codeArr:
        tempArr = listFinderLocal(code)
        for i in range(math.ceil(len(tempArr)/24)*24 - len(tempArr)):
            tempArr.append("###")
        finalTemp1 = []
        for i in range(0, len(tempArr), 3):
            finalTemp1.append([tempArr[i], tempArr[i+1], tempArr[i+2]])
        finalTemp2 = []
        for i in range(0, len(finalTemp1), 8):
            finalTemp2.append([finalTemp1[i], finalTemp1[i+1], finalTemp1[i+2],finalTemp1[i+3], finalTemp1[i+4], finalTemp1[i+5],finalTemp1[i+6], finalTemp1[i+7]])
        render_to_pdf("labelPDF.html", {"code": code, "dataArr": finalTemp2, 'site_key': settings.RECAPTCHA_SITE_KEY})
    onlyfiles = [f for f in listdir("./labels/html/") if isfile(join("./labels/html/", f))]
    for file in onlyfiles :
        pdfkit.from_file("./labels/html/"+file, "./labels/pdf/"+file.split(".html")[0]+'.pdf', configuration=config, options=options)
    zipped_file = zipfile.ZipFile('./labels/labels.zip', 'w')
    onlyfiles = [f for f in listdir("./labels/pdf/") if isfile(join("./labels/pdf/", f))]
    for file in onlyfiles :
        zipped_file.write("./labels/pdf/"+file)
    zipped_file.close()
    return HttpResponse("Done")


def payOneYear(request):
    if request.method == 'POST':
        result_json = gCaptchaVerifer(request.POST['g-recaptcha-response'])
        if not result_json.get('success'):
            response = render(request, "404.html")
            response.status_code = 404
            return response
        else:
            uniqueId = request.POST['uniqueId']
            name = request.POST['name']
            city = request.POST['city']
            taluka = request.POST['taluka']
            district = request.POST['district']
            state = request.POST['state']
            phone = request.POST['phone']
            subYear = int(request.POST['subYear'])
            DATA = {
                "amount": 20000 * subYear,
                "currency": "INR",
                "receipt": "receipt#1",
                "notes": {
                    "uniqueId": uniqueId,
                    "name": name,
                    "city": city,
                    "taluka": taluka,
                    "district": district,
                    "state": state,
                    "phone": phone
                }
            }
            repsonse = client.order.create(data=DATA)
            return HttpResponse(json.dumps(repsonse), content_type="application/json")
