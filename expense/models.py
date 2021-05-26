from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class FixedCostSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/expense/fixed_cost_category/{self.id}/'

    def get_edit_url(self):
        return f'/expense/fixed_cost_category/edit/{self.id}/'

    def get_add_url(self):
        return f'/expense/fixed_cost_category/{self.id}/add_source/'


class FixedCostSource(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE)
    source = models.ForeignKey(FixedCostSourceCategory, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return f'/expense/fixed_cost_source/edit/{self.id}/'


class FixedCosts(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(FixedCostSourceCategory, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(FixedCostSource, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return f'/expense/fixed_costs/edit/{self.id}/'

    def get_date(self):
        return self.date.strftime("%Y-%m-%d")


class VariableCostSourceCategory(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/expense/variable_cost_category/{self.id}/'

    def get_edit_url(self):
        return f'/expense/variable_cost_category/edit/{self.id}/'

    def get_add_url(self):
        return f'/expense/variable_cost_category/{self.id}/add_source/'


class VariableCostSource(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)
    source = models.ForeignKey(VariableCostSourceCategory, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return f'/expense/variable_cost_source/edit/{self.id}/'


class VariableCosts(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(VariableCostSourceCategory, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(VariableCostSource, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return f'/expense/variable_costs/edit/{self.id}/'

    def get_date(self):
        return self.date.strftime("%Y-%m-%d")
