from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class IncomeSource(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name


class IncomeSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE)
    sources = models.ManyToManyField(IncomeSource)

    def __str__(self):
        return self.name


class Income(models.Model):
    amount = models.FloatField()
    description = models.TextField(max_length=128)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=CASCADE)
    category = models.ForeignKey(IncomeSourceCategory, on_delete=CASCADE, null=True)
    source = models.ForeignKey(IncomeSource, on_delete=CASCADE)

    def get_absolute_url(self):
        return f'/income/my_income/edit/{self.id}/'




