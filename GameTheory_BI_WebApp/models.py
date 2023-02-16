from django.db import models


class Rows(models.Model):
    rows_id = models.AutoField(primary_key=True)
    app = models.CharField(max_length=100)
    campaign_network = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    cost = models.CharField(max_length=100)
    partner = models.CharField(max_length=100)
    os_name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    installs = models.IntegerField()


class RowsWeekly(models.Model):
    rows_id = models.AutoField(primary_key=True)
    app = models.CharField(max_length=100)
    campaign_network = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    cost = models.CharField(max_length=100)
    partner = models.CharField(max_length=100)
    os_name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    installs = models.IntegerField()
