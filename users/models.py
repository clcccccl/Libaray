from django.db import models
class User(models.Model):
    name = models.CharField(max_length=30)
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    class_id = models.IntegerField()
    type = models.IntegerField()
    borrow_total = models.IntegerField()
    history_borrow_total = models.IntegerField()

class Class(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class PriceType(models.Model):
    price_type = models.IntegerField()
    price = models.CharField(max_length=200)
    duration = models.IntegerField()
    update =  models.DateTimeField()
    state = models.IntegerField()

# Create your models here.