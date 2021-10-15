from django import forms
# from django.forms import widgets
from .models import Order, Movie

class OrderForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['product_count'].required = True
        self.fields['address'].required = True

    class Meta:
        model = Order
        fields = ['products','product_count','address']

# class CityForm(forms.ModelForm):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         self.fields['name'].required = True

#     class Meta:
#         model = City
#         fields = ['name']
#         widgets = {
#             forms.TextInput(attrs={'class':'input', 'placeholder':'City Name'})
#         }

class MovieForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'].required = True

    class Meta:
        model = Movie
        fields = ['title']