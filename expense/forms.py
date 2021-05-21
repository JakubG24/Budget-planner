from django import forms

from expense.models import FixedCosts, FixedCostSource


class FixedCostForm(forms.ModelForm):
    class Meta:
        model = FixedCosts
        fields = ('amount', 'description', 'date', 'category', 'source')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = FixedCostSource.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['source'].queryset = FixedCostSource.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['source'].queryset = self.instance.category.source_set.order_by('name')