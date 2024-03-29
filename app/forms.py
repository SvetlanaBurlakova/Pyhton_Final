from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.contrib.auth.models import User
from user.models  import User
from .models import Category, Ingredient, IngredientInfo
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from django.forms import formset_factory

#
#
User = get_user_model()


class IngredientForm(forms.Form):
    Ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), label='Выберите ингредиент к добавлению')
    count = forms.IntegerField(label='Введите количество')
    class Meta:
        model = IngredientInfo
        fields = ['Ingredient.name', 'count']


IngredientFormSet = formset_factory(IngredientForm)


class RecipeForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название рецепта')
    description = forms.CharField(widget=forms.Textarea, label='Краткое описание рецепта')
    # ingredients = Ingredient.objects.all()
    steps = forms.CharField(widget=forms.Textarea, label='Шаги приготовления')
    cooking_time = forms.DurationField(label='Общее время приготовления в формате HH:MM:SS')
    author = forms.RadioSelect(attrs={'class': 'form-check-input'})
    image = forms.ImageField(label='Изображение готового блюда', required=False)

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        choices = ((c.name, c.name) for c in categories)
        self.fields['category'] = forms.MultipleChoiceField(choices=choices, label='Категории')


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.CharField(label="Адрес электронной почты")
    author = forms.BooleanField(label="Автор", initial=False, required=False)

    class Meta:
        model = User  # this is the "YourCustomUser" that you imported at the top of the file
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2', 'author')

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True, **kwargs):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            author=self.cleaned_data['author'])
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), label='Имя пользователя')
    password = forms.CharField(widget=PasswordInput(), label='Пароль')


