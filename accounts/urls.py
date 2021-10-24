
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('password_change/', views.password_change, name='password_change'),
    path('edit/', views.profile_edit, name="profile_edit"),
]

"""
login_required라는 장식자를 적용하면 /accounts/login/ 주소로 이동하는데
그 이유는 django/conf/global_settings.py의 LOGIN_URL설정이 '/accounts/login/'이기 때문이다.
"""