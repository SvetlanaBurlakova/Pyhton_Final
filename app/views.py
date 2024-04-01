from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django import forms
from .models import Recipe, Category, Ingredient, IngredientInfo
from .forms import RecipeForm, CustomUserCreationForm, LoginForm, IngredientForm
from random import sample
from user.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.views.generic import RedirectView

# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    result = sample(list(recipes), k=5)
    context = {'title': 'Список рецептов', 'recipes': result}
    return render(request, 'app/index.html', context=context)


def get_recipe(request, recipe_id):
    result = get_object_or_404(Recipe, pk=recipe_id)
    steps = result.steps.split('/')
    ingredients_infos = IngredientInfo.objects.filter(recipe=result).select_related('ingredient').all()
    categories = Category.objects.filter(recipe=result)
    context = {'title': result.name, 'recipe': result, 'steps': steps,
               'categories': categories, 'ingredients_infos': ingredients_infos}
    return render(request, 'app/recipe.html', context=context)


def get_recipe_auth(request, recipe_id):
    result = get_object_or_404(Recipe, pk=recipe_id)
    ingredients_infos = IngredientInfo.objects.filter(recipe=result).select_related('ingredient').all()
    categories = Category.objects.filter(recipe=result)
    context = {'title': result.name, 'recipe': result, 'categories': categories, 'recipe_id': recipe_id,
               'ingredients_infos': ingredients_infos}
    return render(request, 'app/recipe_auth.html', context=context)


def category(request, category_id):
    category= get_object_or_404(Category, pk=category_id)
    recipes = Recipe.objects.filter(category=category).all()
    context = {'title': category.name, 'recipes': recipes}
    return render(request, 'app/category.html', context=context)


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            if image is not None:
                fs = FileSystemStorage()
                fs.save(image.name, image)
            author = User.objects.get(pk=request.user.id)
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            steps = form.cleaned_data['steps']
            cooking_time = form.cleaned_data['cooking_time']
            categories = form.cleaned_data['category']
            categories_set = set(Category.objects.get(name=c) for c in categories)
            recipe = Recipe(name=name, description=description, steps=steps, cooking_time=cooking_time,
                   image=image, author=author)
            recipe.save()
            for categoryEntity in categories_set:
                recipe.category.add(categoryEntity)
            recipe.save()
            context ={'title': name, 'recipe': recipe, 'steps':steps,
               'categories':categories_set}
            return render(request, 'app/recipe_auth.html', context=context)

    else:
        form = RecipeForm()
    context = {
        'title': 'Добавление рецепта',
        'form': form,
    }
    return render(request, 'app/add_recipe.html', context=context)


def change_recipe(request, recipe_id):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            if image:
                fs = FileSystemStorage()
                fs.save(image.name, image)
            author = User.objects.get(pk=request.user.id)
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            steps = form.cleaned_data['steps']
            cooking_time = form.cleaned_data['cooking_time']
            categories = form.cleaned_data['category']
            categories_set = set(Category.objects.get(name=c) for c in categories)
            recipe = Recipe(name=name, description=description, steps=steps, cooking_time=cooking_time,
                            image=image, author=author)
            recipe.save()
            for categoryEntity in categories_set:
                recipe.category.add(categoryEntity)
            recipe.save()
            Recipe.objects.filter(pk=recipe_id).update(name=name, description=description, steps=steps, cooking_time=cooking_time,
                            image=image, author=author)
            context = {'title': name, 'recipe': recipe, 'categories': categories_set}
            return render(request, 'app/recipe_auth.html', context=context)

    else:
        result = get_object_or_404(Recipe, pk=recipe_id)
        form = RecipeForm()
        form.fields['name'] = forms.CharField(initial=result.name, label='Название рецепта')
        form.fields['description'] = forms.CharField(widget=forms.Textarea, initial=result.description, label='Краткое описание рецепта')
        form.fields['steps'] = forms.CharField(widget=forms.Textarea, initial=result.steps, label='Шаги приготовления')
        form.fields['cooking_time'] = forms.DurationField(initial=result.cooking_time, label='Общее время приготовления в формате HH:MM:SS')
        form.fields['image'] = forms.ImageField(initial=result.image, label='Изображение готового блюда', required=False)
    context = {
        'title': 'Изменение рецепта',
        'form': form,
    }
    return render(request, 'app/change_recipe.html', context=context)


def delete_recipe(request, recipe_id):
    Recipe.objects.filter(pk=recipe_id).delete()
    print(recipe_id)
    user = User.objects.get(pk=request.user.id)
    recipes = Recipe.objects.filter(author=user).all()
    if len(recipes) == 0:
        recipes = sample(list(Recipe.objects.all()), k=2)
        context = {'title': 'Рецепт удален, У вас нет больше загруженных рецептов', 'recipes': []}
    else:
        context = {'title': 'Рецепт удален', 'recipes': recipes}
    return render(request, 'app/index_login_author.html', context=context)


def get_recipes_by_author(request, author_id):
    user = get_object_or_404(User, pk=author_id)
    recipes = Recipe.objects.filter(author=user).all()
    if len(recipes) == 0:
        recipes = sample(list(Recipe.objects.all()), k=5)
        context ={'title': 'У вас нет загруженных рецептов', 'recipes': []}
    else:
        context = {'title': 'Список ваших рецептов', 'recipes': recipes}
    return render(request, 'app/index_login_author.html', context=context)


def get_recipes(request):
    recipes = sample(list(Recipe.objects.all()), k=5)
    context = {'title': 'Список рецептов', 'recipes': recipes}
    return render(request, 'app/index.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            recipes = Recipe.objects.all()
            result = sample(list(recipes), k=5)
            context = {'title': 'Список рецептов', 'recipes': result}
            return render(request, 'app/index.html', context=context)
    else:
        form = CustomUserCreationForm()
    context = {'form':form}
    return render(request, 'app/registration.html', context)


def signin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                if user.author:
                    recipes = Recipe.objects.filter(author=user).all()
                    if len(recipes) == 0:
                        #recipes = sample(list(Recipe.objects.all()), k=5)
                        recipes = []
                    context = {'title': 'Добро пожалывать на наш сайт!', 'recipes': recipes}
                    return render(request, 'app/index_login_author.html', context=context)
                else:
                    recipes = sample(list(Recipe.objects.all()), k=5)
                    context = {'title': 'Добро пожалывать на наш сайт!', 'recipes': recipes}
                    return render(request, 'app/index_login.html', context=context)
    context = {'title':'Авторизация пользователя','form': form}
    return render(request, 'app/login.html', context=context)


def logout_view(request):
    logout(request)
    return index(request)


def add_ingredient_to_the_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.cleaned_data['Ingredient']
            count = form.cleaned_data['count']
            ingredient_info = IngredientInfo(recipe_id=recipe_id, ingredient_id=ingredient.id, count=count)
            ingredient_info.save()
            result = get_object_or_404(Recipe, pk=recipe_id)
            ingredients_infos = IngredientInfo.objects.filter(recipe=result).select_related('ingredient').all()
            categories = Category.objects.filter(recipe=result)
            context = {'title': result.name, 'recipe': result, 'categories': categories, 'recipe_id': recipe_id,
                       'ingredients_infos': ingredients_infos}
            return render(request, 'app/recipe_auth.html', context=context)
    else:
        form = IngredientForm()
        context = {'title': f'Добавление нового ингредиента к рецепту {recipe.name}', 'form': form}
        return render(request, 'app/add_ingredient.html', context=context)


def delete_ingredient(request, recipe_id, info_id):
    IngredientInfo(pk=info_id).delete()
    result = get_object_or_404(Recipe, pk=recipe_id)
    ingredients_infos = IngredientInfo.objects.filter(recipe=result).select_related('ingredient').all()
    categories = Category.objects.filter(recipe=result)
    context = {'title': result.name, 'recipe': result, 'categories': categories, 'recipe_id': recipe_id,
               'ingredients_infos': ingredients_infos}
    return render(request, 'app/recipe_auth.html', context=context)


