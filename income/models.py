from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class IncomeSource(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class IncomeSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ManyToManyField(IncomeSource)


class Income(models.Model):
    amount = models.FloatField()
    description = models.TextField(max_length=128)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ForeignKey(IncomeSource, on_delete=CASCADE)

    def get_absolute_url(self):
        return f'/income/my_income/edit/{self.id}/'




