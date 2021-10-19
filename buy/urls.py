from django.urls import path
from . import views

app_name = 'buy'

urlpatterns =[
    path('order/', views.order, name="order"),
    path('detail/', views.order_detail, name="order_detail"),
    path('discard/', views.order_discard, name="order_discard"),
    path('recommends/', views.recommends, name="recommends"),
]