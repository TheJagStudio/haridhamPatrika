from django.db import models
from django.utils import timezone


class Pradesh(models.Model):
    pradeshName = models.CharField(max_length=100)

    def __str__(self):
        return self.pradeshName


class State(models.Model):
    stateName = models.CharField(max_length=100)

    def __str__(self):
        return self.stateName


class District(models.Model):
    districtName = models.CharField(max_length=100)
    districtCode = models.CharField(max_length=6, null=True,blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.districtName


class Taluka(models.Model):
    talukaName = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.talukaName


class City(models.Model):
    cityName = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE)
    pradesh = models.ForeignKey(Pradesh, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.cityName


class Zone(models.Model):
    zoneName = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.zoneName


class BhagatDetail(models.Model):
    districtCode = models.CharField(max_length=6, null=True,blank=True)
    disCount = models.CharField(max_length=6, null=True,blank=True)
    dataid = models.CharField(max_length=6, null=True,blank=True)
    receiptNo = models.CharField(max_length=15, null=True,blank=True)
    receiptDate = models.DateField(default=timezone.now, null=True,blank=True)
    entryDate = models.DateField(default=timezone.now, null=True,blank=True)
    startDate = models.DateField()
    endDate = models.DateField()
    subYear = models.IntegerField()
    name = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField(max_length=254, null=True,blank=True)
    addressOne = models.CharField(max_length=100, null=True,blank=True)
    addressTwo = models.CharField(max_length=100, null=True,blank=True)
    addressThree = models.CharField(max_length=100, null=True,blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True,blank=True)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE, null=True,blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True,blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True,blank=True)
    is_zone = models.BooleanField()
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True,blank=True)
    pradesh = models.ForeignKey(Pradesh, on_delete=models.CASCADE, null=True,blank=True)
    phoneNum = models.CharField(max_length=10, null=True,blank=True)
    newFlag = models.BooleanField()
    dontSendFlag = models.BooleanField()
    pincode = models.CharField(max_length=6, null=True,blank=True)
    remark = models.CharField(max_length=100, null=True,blank=True)
    is_active = models.BooleanField()
    redZone = models.BooleanField(default=False)
    qrcode = models.CharField(max_length=10000, null=True,blank=True,default="")

    def __str__(self):
        return self.name


class Karyakarta(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phoneNum = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
