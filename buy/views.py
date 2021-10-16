from django.shortcuts import render,redirect
from .forms import OrderForm, MovieForm
from django.utils import timezone
from django.contrib import messages
from .models import Order, Movie
from django.contrib.auth.decorators import login_required
from .modeling import get_recommendations, overviews
import pandas as pd
# import pickle
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
                return redirect('buy:recommends')
    else:
        form = OrderForm()
    
    context = {'form':form}
    return render(request,"buy/order_form.html",context)

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 주문 내역 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
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



#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 추천2 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

@login_required
def recommends(request):
    if request.method == "POST":
        Movies = Movie.objects.all().filter(user=request.user)
        if len(Movies) >= 1:
            Movies.delete()
        else:
            pass
        form = MovieForm(request.POST)
        if form.is_valid:
            m = form.save(commit=False)
            m.user = request.user
            m.save()
            return redirect('buy:recommends')

    form = MovieForm()
    movies = Movie.objects.last() 
    # pickle사용
    # with open('get_recommendations', 'rb') as f:
    #     recommendation = pickle.load(f) 

    try:
        # pred = recommendation(movies.title) # pickle사용할 경우
        pred = get_recommendations(movies.title)
        final = pd.DataFrame(pred)

        movies_title = movies.title 
        recommend_mv = final.title
        ove = overviews.loc[movies.title].overview
        release_date = overviews.loc[movies.title].release_date
        runtime = int(overviews.loc[movies.title].runtime)
        vote_average = overviews.loc[movies.title].vote_average
        genres	= overviews.loc[movies.title].genres	

        context = {
            'form':form,
            'movies_title':movies_title,
            'recommend_mv':recommend_mv,
            'ove':ove,
            'release_date':release_date,
            'runtime':runtime,
            'vote_average':vote_average,
            'genres':genres
        }

        return render(request, 'buy/movie_test.html',context)

    except:
        context = {
            'form':form,
        }

        return render(request, 'buy/movie_main.html',context)

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 추천 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

# @login_required
# def recommend(request):
#     if request.method == "POST":
#         cities = City.objects.all().filter(user=request.user)
#         if len(cities) >= 1:
#             cities.delete()
#         else:
#             pass
#         form = CityForm(request.POST)
#         if form.is_valid:       
#             k = form.save(commit=False)
#             k.user = request.user
#             k.save()
#             return redirect("buy:recommend")

#     form = CityForm()

#     cities = City.objects.all().filter(user=request.user)

#     weather_data,comments = [],[]
#     for city in cities:
#         url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=170042f861af86da70b4e4b96749b810&lang=kr'
#         r = requests.get(url).json()
#         print(r)
#         city_weather = {
#             'city' : city.name,
#             'temperature' : round(r['main']['temp']- 273.15,1),
#             'description' : r['weather'][0]['description'],
#             'icon' : r['weather'][0]['icon']
#         }
#         weather_data.append(city_weather)


#         if '흐림' in city_weather['description']:
#             comment = "오늘은 구름이 많이 꼈네요! 집에서 한잔 해야 할것 같아요~"
#             comments.append(comment)
#         elif '맑음' in city_weather['description']:
#             comment = "오늘은 화창하군요~! 친구들과 공원에서 한잔 어때요~?!"
#             comments.append(comment)
#         elif '비' in city_weather['description']:
#             comment = "오늘은 비가오네요ㅠㅠ! 오늘은 전에 막걸리 고고~!"
#             comments.append(comment)
#         elif '구름' in city_weather['description']:
#             comment = "오늘은 구름이 많이 꼈네요! 집에서 한잔 해야 할것 같아요~"
#             comments.append(comment)
#         else:
#             pass

#     # 상품 추천
#     product_list = Product.objects.all()
#     pick = random.choice(product_list)
#     context = {
#                 'product_list':product_list,
#                 'pick':pick,
#                 'weather_data' : weather_data,
#                 'form':form,
#                 'comments' : comments,
#                 }
#     return render(request, 'buy/recommend.html',context)