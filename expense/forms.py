from django import forms
from django.contrib.auth.models import User
from django.forms import NumberInput
from django.template.context_processors import request

from expense.models import FixedCosts, FixedCostSource, VariableCostSource, VariableCosts


class FixedCostForm(forms.ModelForm):
    amount = forms.FloatField(min_value=0)

    class Meta:
        model = FixedCosts
        fields = ['category', 'source', 'amount', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(FixedCostForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = FixedCostSource.objects.none()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['source'].queryset = FixedCostSource.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['source'].queryset = self.instance.category.source_set.order_by('name')


class VariableCostForm(forms.ModelForm):
    amount = forms.FloatField(min_value=0)

    class Meta:
        model = VariableCosts
        fields = ['category', 'source', 'amount', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(VariableCostForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = VariableCostSource.objects.none()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['source'].queryset = VariableCostSource.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['source'].queryset = self.instance.category.source_set.order_by('name')