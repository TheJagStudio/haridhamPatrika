from django.db import models
from django.contrib.auth.models import User

# name
# pradesh
# address
# email
# phone1
# phone2
# GST No
# Pan No

# ads details :
# - single/ multiple
# - ads description
# - logo
# - extra files (coral, pdf, photoshop,AI,...)
# - extra description
# - old photo

# payment:
# - mode (online/check/cash)
# - single : 20
# - multi : 50

# online

# check:
# - bank name
# - check number
# - amount
# - account holder name

# cash:
# - amount
# - date
# - repcit no
# - reference name/number


class CalendarUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, blank=True, null=True)
    pradesh = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    isKaryakata = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class CalendarEntry(models.Model):
    def filePath(self):
        return f"media/{self.user.user.first_name}_{self.user.user.last_name}_{self.user.user.id}/"

    user = models.ForeignKey(CalendarUser, on_delete=models.CASCADE)
    adDescription = models.CharField(max_length=2000, blank=True, null=True)
    logo = models.CharField(max_length=500, blank=True, null=True)
    extraFiles = models.JSONField(default=dict, blank=True, null=True)
    extraDescription = models.CharField(max_length=2000, blank=True, null=True)
    oldPhoto = models.CharField(max_length=500, blank=True, null=True)
    paymentMode = models.CharField(max_length=10, blank=True, null=True)
    paymentId = models.CharField(max_length=100,blank=True, null=True)
    onlinePaymentDetails = models.JSONField(default=dict, blank=True, null=True)
    singleCount = models.IntegerField(blank=True, null=True)
    multiCount = models.IntegerField(blank=True, null=True)
    bankName = models.CharField(max_length=100, blank=True, null=True)
    chequeNumber = models.CharField(max_length=100, blank=True, null=True)
    totalAmount = models.IntegerField(blank=True, null=True)
    accountHolderName = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    receiptNumber = models.CharField(max_length=100, blank=True, null=True)
    referenceName = models.CharField(max_length=100, blank=True, null=True)
    referenceNumber = models.CharField(max_length=100, blank=True, null=True)
    gstNo = models.CharField(max_length=10, blank=True, null=True)
    panNo = models.CharField(max_length=10, blank=True, null=True)
    isPaid = models.BooleanField(default=False, blank=True, null=True)
    isApproved = models.BooleanField(default=False, blank=True, null=True)
    isProcessing = models.BooleanField(default=False, blank=True, null=True)
    isPrinted = models.BooleanField(default=False, blank=True, null=True)
    isDelivered = models.BooleanField(default=False, blank=True, null=True)
    isRejected = models.BooleanField(default=False, blank=True, null=True)
    isDeleted = models.BooleanField(default=False, blank=True, null=True)
    isCompleted = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return (
            self.user.user.first_name+" "+self.user.user.last_name + " (" + self.paymentMode+")"
        )
