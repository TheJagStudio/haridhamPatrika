# Generated by Django 4.1.3 on 2022-11-28 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_bhagatdetail_dataid'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='pradesh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.pradesh'),
        ),
    ]