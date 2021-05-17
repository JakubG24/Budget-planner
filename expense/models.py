from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class FixedCostSource(models.Model):
    name = models.CharField(max_length=64)


class FixedCostSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ManyToManyField(FixedCostSource)


class FixedCosts(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(max_length=128)
    user = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ForeignKey(FixedCostSource, on_delete=CASCADE)
