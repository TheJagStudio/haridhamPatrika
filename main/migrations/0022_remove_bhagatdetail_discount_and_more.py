# Generated by Django 4.1.4 on 2023-07-27 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0021_remove_bhagatdetail_city_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="bhagatdetail", name="disCount",),
        migrations.RemoveField(model_name="bhagatdetail", name="dontSendFlag",),
        migrations.RemoveField(model_name="bhagatdetail", name="redZone",),
    ]
