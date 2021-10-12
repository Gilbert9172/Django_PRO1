from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['product_count'].required = True
        self.fields['address'].required = True

    class Meta:
        model = Order
        fields = ['products','product_count','address']