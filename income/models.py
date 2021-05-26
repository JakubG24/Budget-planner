from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class IncomeSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name


class IncomeSource(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE)
    categories = models.ManyToManyField(IncomeSourceCategory)

    def __str__(self):
        return self.name


class Income(models.Model):
    amount = models.FloatField()
    description = models.TextField(max_length=128)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(IncomeSourceCategory, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(IncomeSource, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return f'/income/my_income/edit/{self.id}/'

    def get_date(self):
        return self.date.strftime("%Y-%m-%d")




