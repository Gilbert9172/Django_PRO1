from django import forms
from django.forms import widgets
from .models import City, Order

class OrderForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['product_count'].required = True
        self.fields['address'].required = True

    class Meta:
        model = Order
        fields = ['products','product_count','address']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            forms.TextInput(attrs={'class':'input', 'placeholder':'City Name'})
        }