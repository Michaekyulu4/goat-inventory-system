from django import forms
from .models import Goat, DeathRecord, SaleRecord


class GoatForm(forms.ModelForm):
    class Meta:
        model = Goat
        fields = [
            'tag_number',
            'gender',
            'date_of_birth',
            'mother',
            'image',
            'date_bought',
            'purchase_price'
        ]
        widgets = {
            'tag_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mother': forms.Select(attrs={'class': 'form-control'}),
            'date_bought': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
class DeathRecordForm(forms.ModelForm):

    class Meta:
        model = DeathRecord
        fields = ['date_of_death', 'cause']

        widgets = {
            'date_of_death': forms.DateInput(attrs={'type': 'date'})
        }

class SaleRecordForm(forms.ModelForm):

    class Meta:
        model = SaleRecord

        fields = ['date_sold', 'sale_price']

        widgets = {
            'date_sold': forms.DateInput(attrs={'type': 'date'})
        }