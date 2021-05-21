from django import forms
from income.models import Income


class IncomeForm(forms.ModelForm):
    amount = forms.FloatField(min_value=0)

    class Meta:
        model = Income
        fields = ['amount', 'date', 'description', 'category', 'source']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }