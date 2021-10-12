from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 SignupForm 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
# from django.contrib.auth import get_user_model
# User = get_user_model()
# user = User.objects.first()
# user => <User: gilbert>

# user.password = '1234' 그대로 반환
# user.set_password('1234') 암호화 되서 반환

# UserCreationForm에서 회원가입이 구현되어있다.
class SignupForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].required = True
        self.fields['gender'].required = True
        self.fields['age'].required = True
        self.fields['phone_number'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ['username','gender','age','phone_number','email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email



#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 ProfileForm 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields =  ['address','phone_number','email']



#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 PasswordChangeForm 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        new_password2 = super().clean_new_password2()
        if old_password == new_password2:
            raise forms.ValidationError(
                "이전과 동일한 암호 입니다."
            )
        return new_password2 

# new_password1 = self.cleaned_data.get('new_password1')
# if old_password and new_password1
# if old_password == new_password1
# raise forms.ValidationError