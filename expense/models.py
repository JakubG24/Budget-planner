from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class FixedCostSource(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name


class FixedCostSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE)
    sources = models.ForeignKey(FixedCostSource, on_delete=CASCADE, null=True)
    
    def __str__(self):
        return self.name


class FixedCosts(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(max_length=128)
    user = models.ForeignKey(User, on_delete=CASCADE)
    category = models.ForeignKey(FixedCostSourceCategory, on_delete=CASCADE, null=True)
    source = models.ForeignKey(FixedCostSource, on_delete=CASCADE)

    def get_absolute_url(self):
        return f'/expense/fixed_costs/edit/{self.id}/'

class VariableCostSource(models.Model):
    name = models.CharField(max_length=64)


class VariableCostSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ManyToManyField(FixedCostSource)


class VariableCosts(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(max_length=128)
    user = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ForeignKey(FixedCostSource, on_delete=CASCADE)
