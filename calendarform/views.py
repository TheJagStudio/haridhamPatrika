from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import CalendarEntry, CalendarUser
import razorpay
import os
import uuid
import datetime

client = razorpay.Client(auth=("rzp_test_EdIMHRHA7suoML", "RBJc7ZCTLEBky3n2To6UyufG"))


def register(request):
    if request.method == "POST":
        fName = request.POST.get("fName")
        lName = request.POST.get("lName")
        email = request.POST.get("email")
        phoneNumber = request.POST.get("phoneNumber")
        whatsappNumber = request.POST.get("whatsappNumber")
        pradesh = request.POST.get("pradesh")
        address = request.POST.get("address")
        password = request.POST.get("password")

        getUser = User.objects.filter(username=phoneNumber)
        if getUser:
            context = {"error": "User already exists"}
            return render(request, "register.html", context=context)
        else:
            try:
                newUser = User()
                newUser.first_name = fName
                newUser.last_name = lName
                newUser.email = email
                newUser.username = phoneNumber
                newUser.set_password(password)
                newUser.save()

                newCalendarUser = CalendarUser()
                newCalendarUser.user = newUser
                newCalendarUser.address = address
                newCalendarUser.pradesh = pradesh
                newCalendarUser.mobile = phoneNumber
                newCalendarUser.whatsapp = whatsappNumber
                newCalendarUser.save()
                context = {"success": "User created successfully"}
                return render(request, "register.html", context=context)
            except Exception as e:
                context = {"error": str(e)}
                return render(request, "calendarRegister.html", context=context)
    return render(request, "calendarRegister.html")


def signin(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect("/calendar/")
        else:
            context = {"error": "Invalid Credentials"}
            return render(request, "calendarLogin.html", context=context)
    return render(request, "calendarLogin.html")


@login_required(login_url="/calendar/login/")
def home(request):
    entrys = CalendarEntry.objects.filter(user__user=request.user)
    entryArr = []
    for entry in entrys:
        temp = {}
        temp["id"] = entry.id
        temp["date"] = entry.date
        temp["logo"] = entry.logo
        temp["adDescription"] = entry.adDescription
        temp["singleCount"] = entry.singleCount
        temp["multiCount"] = entry.multiCount
        temp["paymentMode"] = entry.paymentMode
        temp["totalAmount"] = entry.totalAmount
        temp["gstNo"] = entry.gstNo
        temp["panNo"] = entry.panNo
        temp["isPaid"] = entry.isPaid

        if entry.isApproved:
            temp["status"] = "Approved"
        else:
            temp["status"] = "Approve Pending"
        if entry.isProcessing:
            temp["status"] = "Processing"
        if entry.isPrinted:
            temp["status"] = "Printed"
        if entry.isDelivered:
            temp["status"] = "Delivered"
        if entry.isRejected:
            temp["status"] = "Rejected"
        if entry.isDeleted:
            temp["status"] = "Deleted"
        if entry.isCompleted:
            temp["status"] = "Completed"

        entryArr.append(temp)
    context = {
        "name": request.user.first_name + " " + request.user.last_name,
        "orders": entryArr,
        "hasOrder": len(entryArr),
    }
    return render(request, "calendarHome.html", context=context)


@login_required(login_url="/calendar/login/")
def order(request):
    if request.method == "POST":
        logoFile = request.FILES.get("logo", False)
        extraFiles = request.FILES.getlist("extraFiles")
        oldPhoto = request.FILES.get("oldPhoto", False)

        allfilesList = os.listdir("media/userData")
        folderName = (
            request.user.first_name
            + "_"
            + request.user.last_name
            + "_"
            + request.user.username
        )
        if folderName not in allfilesList:
            os.mkdir("media/userData/" + folderName)

        if logoFile:
            with open(
                "media/userData/" + folderName + "/" + logoFile.name, "wb+"
            ) as destination:
                for chunk in logoFile.chunks():
                    destination.write(chunk)
            request.session["logo"] = (
                "/media/userData/" + folderName + "/" + logoFile.name
            )
        if len(extraFiles) > 0:
            temp = []
            for extraFile in extraFiles:
                with open(
                    "media/userData/" + folderName + "/" + extraFile.name, "wb+"
                ) as destination:
                    for chunk in extraFile.chunks():
                        destination.write(chunk)
                temp.append("/media/userData/" + folderName + "/" + extraFile.name)
            request.session["extraFiles"] = temp
        if oldPhoto:
            with open(
                "media/userData/" + folderName + "/" + oldPhoto.name, "wb+"
            ) as destination:
                for chunk in oldPhoto.chunks():
                    destination.write(chunk)
            request.session["oldPhoto"] = (
                "/media/userData/" + folderName + "/" + oldPhoto.name
            )

        singleCount = request.POST.get("singleCount")
        multiCount = request.POST.get("multiCount")
        adDescription = request.POST.get("adDescription")
        extraDescription = request.POST.get("extraDescription")
        gstNo = request.POST.get("gstNo")
        panNo = request.POST.get("panNo")
        request.session["singleCount"] = singleCount
        request.session["multiCount"] = multiCount
        request.session["adDescription"] = adDescription
        request.session["extraDescription"] = extraDescription
        request.session["gstNo"] = gstNo
        request.session["panNo"] = panNo

        currentUser = User.objects.get(username=request.user.username)
        calendarUserCurrent = CalendarUser.objects.filter(user=currentUser).first()

        finalAmount = 0
        if singleCount != "":
            finalAmount += int(singleCount) * 20
        if multiCount != "":
            finalAmount += int(multiCount) * 50

        DATA = {
            "amount": finalAmount * 100,
            "currency": "INR",
            "receipt": "receipt#" + str(calendarUserCurrent.id),
            "notes": {
                "name": request.user.first_name + " " + request.user.last_name,
                "adDescription": adDescription,
                "extraDescription": extraDescription,
                "pradesh": calendarUserCurrent.pradesh,
                "phone": calendarUserCurrent.mobile,
            },
        }
        repsonse = client.order.create(data=DATA)
        request.session["paymentDetails"] = repsonse
        return redirect("payment")
    return render(request, "calendarOrder.html")


@login_required(login_url="/calendar/login/")
def payment(request):
    if request.method == "POST":
        paymentMode = request.POST.get("paymentMode")

        newCalendarEntry = CalendarEntry()
        newCalendarEntry.user = CalendarUser.objects.get(user=request.user)
        newCalendarEntry.adDescription = request.session.get("adDescription")
        newCalendarEntry.logo = request.session.get("logo")
        newCalendarEntry.extraFiles = request.session.get("extraFiles")
        newCalendarEntry.extraDescription = request.session.get("extraDescription")
        newCalendarEntry.oldPhoto = request.session.get("oldPhoto")
        newCalendarEntry.paymentMode = paymentMode
        newCalendarEntry.gstNo = request.session.get("gstNo")
        newCalendarEntry.panNo = request.session.get("panNo")

        finalAmount = 0
        if request.session["singleCount"] != "":
            finalAmount += int(request.session["singleCount"]) * 20
        if request.session["multiCount"] != "":
            finalAmount += int(request.session["multiCount"]) * 50
        newCalendarEntry.totalAmount = finalAmount

        if request.session["singleCount"] != "":
            newCalendarEntry.singleCount = request.session.get("singleCount")
        if request.session["multiCount"] != "":
            newCalendarEntry.multiCount = request.session.get("multiCount")

        if paymentMode == "cheque":
            chequeNumber = request.POST.get("chequeNumber")
            bankName = request.POST.get("bankName")
            accountholdername = request.POST.get("accountHolderName")
            chequeDate = request.POST.get("chequeDate")

            newCalendarEntry.chequeNumber = chequeNumber
            newCalendarEntry.bankName = bankName
            newCalendarEntry.accountHolderName = accountholdername
            newCalendarEntry.date = chequeDate
        elif paymentMode == "cash":
            date = request.POST.get("date")
            reciptNo = request.POST.get("reciptNo")
            refName = request.POST.get("refName")
            refNumber = request.POST.get("refNumber")

            newCalendarEntry.date = date
            newCalendarEntry.receiptNumber = reciptNo
            newCalendarEntry.referenceName = refName
            newCalendarEntry.referenceNumber = refNumber
        else:
            razorpayPaymentId = request.POST.get("razorpayPaymentId")

            newCalendarEntry.paymentId = razorpayPaymentId
            newCalendarEntry.onlinePaymentDetails = request.session.get(
                "paymentDetails"
            )
            newCalendarEntry.isPaid = True
            newCalendarEntry.date = datetime.datetime.now()

        newCalendarEntry.save()

        del request.session["singleCount"]
        del request.session["multiCount"]
        del request.session["paymentDetails"]

        return redirect("home")

    if request.session.get("paymentDetails") == None:
        return redirect("home")
    calendarUserCurrent = CalendarUser.objects.get(user=request.user)
    # name amount
    finalAmount = 0
    if request.session["singleCount"] != "":
        finalAmount += int(request.session["singleCount"]) * 20
    if request.session["multiCount"] != "":
        finalAmount += int(request.session["multiCount"]) * 50
    context = {
        "name": request.user.first_name + " " + request.user.last_name,
        "email": request.user.email,
        "amount": finalAmount * 100,
        "amountRupee": finalAmount,
        "pradesh": calendarUserCurrent.pradesh,
        "paymentDetails": request.session.get("paymentDetails"),
    }
    return render(request, "calendarPayment.html", context=context)
