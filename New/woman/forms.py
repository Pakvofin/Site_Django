from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField




from .models import *

class AddPostForm(forms.ModelForm): #Наслідування базового класу Form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категорію не вибрано'
    class Meta:
        model = Woman
        fields = ['title', 'slug', 'content','photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 150:
            raise ValidationError('Довжина перевищує 200 символів')
        return title



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-input'}))

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input'}))

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-input'}))

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ContactForm(forms.Form):
    name = forms.CharField(label='Ім\'я', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(
        label='Коментар',
        widget=forms.Textarea(
            attrs={'cols': 60, 'rows':10}
        )
    )
    captcha = CaptchaField()


#     title = forms.CharField(max_length=255, label='Заголовок',
#                             widget=forms.TextInput(
#                                 attrs={'class': 'form-input'}))
# #label - зміна назви поля на сайті
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(
#         attrs={'cols': 60, 'rows': 10}), label='Біографія')
#     is_published = forms.BooleanField(label='Стан публікації',
#                                       required=False,
#                                       initial=True)
# #required - робить поле is_published не обов'язковим до заповнення
# #initial - автоматично відмічає (заповнює) поле
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(),
#                                  label='Розділ',
#                                  empty_label='Категорію не вибрано')
# #empty_label - перейменовує стандартну стріку з -----