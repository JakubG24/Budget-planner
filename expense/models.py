from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class FixedCostSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'expense_fixedcostsourcecategory'


class FixedCostSource(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ForeignKey(FixedCostSourceCategory, on_delete=CASCADE, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'expense_fixedcostsource'


class FixedCosts(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(max_length=128)
    user = models.ForeignKey(User, on_delete=CASCADE)
    category = models.ForeignKey(FixedCostSourceCategory, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(FixedCostSource, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'expense_fixedcosts'

    def get_absolute_url(self):
        return f'/expense/fixed_costs/edit/{self.id}/'

    def get_date(self):
        return self.date.strftime("%Y-%m-%d")


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
