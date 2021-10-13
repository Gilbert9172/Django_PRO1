from django.shortcuts import render,redirect
from .forms import OrderForm, CityForm
from django.utils import timezone
from django.contrib import messages
from .models import City, Order, Product
from django.contrib.auth.decorators import login_required
import random, requests
# from django.shortcuts import get_object_or_404
# from django.contrib.auth import get_user_model


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 주문 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

@login_required
def order(request):
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
                ordering = form.save(commit=False)
                ordering.order_time = timezone.now()
                ordering.user = request.user
                ordering.save()
                messages.success(request,"주문을 성공하셨습니다")
                return redirect('root')
    else:
        form = OrderForm()
    
    context = {'form':form}
    return render(request,"buy/order_form.html",context)

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 주문 내역 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

# @login_required
# def order_detail(request):
#     order_list = Order.objects.filter(user_id=request.user.id)
#     context = {'order':order_list}
#     return render(request,'buy/order_detail.html',context)

@login_required
def order_detail(request):
    # request.user의 주문 목록 모두 가져오기.
    order_list = Order.objects.filter(user=request.user)
    context = {'order_list':order_list}
    return render(request,'buy/order_detail.html',context)


# @login_required
# def order_change(request):
#     if request.method =="POST":
#         form = OrderForm(request.POST, instance=request.user)
#         if form.is_valid():
#             ordering = form.save(commit=False)
#             ordering.order_time = timezone.now()
#             # ordering.user = request.user
#             ordering.save()
#     else:
#         form = OrderForm(instance=request.user)

    # context = {'form':form}
    # return render(request,"buy/order_form.html",context)

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 주문 취소 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

@login_required
def order_discard(request):
    order = Order.objects.filter(user_id=request.user.id)
    order.delete()
    messages.success(request,"주문을 취소했습니다.")
    return redirect("root")

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 추천 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

@login_required
def recommend(request):

    # 날씨 가져오기
    url = 'http://api.openweathermap.org/data/2.5/weather?id=524901&lang=kr&appid=7d99cbf41595e294aeb700bfbe487ff7'

    if request.method == "POST":
        form = CityForm(request.POST)        
        k = form.save(commit=False)
        k.user = request.user
        k.save()

    form = CityForm()

    cities = City.objects.all().filter(user=request.user)
    cities = cities[:1]
    weather_data = []
    comments = []
    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : round(r['main']['temp']- 273.15,1),
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }
        weather_data.append(city_weather)


        if '흐림' in city_weather['description']:
            comment = "오늘은 구름이 많이 꼈네요! 집에서 한잔 해야 할것 같아요~"
            comments.append(comment)
        elif '맑음' in city_weather['description']:
            comment = "오늘은 화창하군요~! 친구들과 공원에서 한잔 어때요~?!"
            comments.append(comment)
        else:
            pass

    # 상품 추천
    product_list = Product.objects.all()
    pick = random.choice(product_list)
    context = {
                'product_list':product_list,
                'pick':pick,
                'weather_data' : weather_data,
                'form':form,
                'comments' : comments,
                }
    return render(request, 'buy/recommend.html',context)