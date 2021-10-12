from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm,PasswordChangeForm
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView as AuthPasswordChangeView)
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 회원가입 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request,"회원가입을 환영합니다.")
            next_url = request.GET.get('next','/')
            return redirect(next_url)
    else:
        form = SignupForm()
    context = {'form':form}
    return render(request,'accounts/signup_form.html', context)



#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 로그인 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
# 사실 loginview는 django.auth에 구현이 되어있다. 
# def login(request):
#     pass
# 별도의 logic이 필요한 경우 위와 같이 함수기반 view로 구현 
# 아니면 class기반으로 할 수 있다.

login = LoginView.as_view(template_name ="accounts/login_form.html")



#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 로그아웃 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
# logout = LogoutView.as_view(template_name="accounts/logout_form.html")
# def logout(request):
#     messages.success(request, "로그아웃 되었습니다.")
#     return logout_then_login(request)
logout = auth_views.LogoutView.as_view()

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 프로필 수정 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
@login_required
def profile_edit(request):
    if request.method == "POST":    
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"프로필을 수정했습니다.")
            return redirect("root")
    else:
        form = ProfileForm(instance=request.user)


    return render(request,'accounts/profile_edit_form.html',{'form':form})


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 비밀번호 수정 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self,form):
        messages.success(self.request,"암호를 변경했습니다.")
        return super().form_valid(form)

password_change = PasswordChangeView.as_view()