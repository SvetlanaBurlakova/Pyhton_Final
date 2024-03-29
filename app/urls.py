from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>', views.get_recipe, name='recipe'),
    path('recipe_auth/<int:recipe_id>', views.get_recipe_auth, name='recipe_auth'),
    path('category/<int:category_id>', views.category, name='category'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('change_recipe/<int:recipe_id>', views.change_recipe, name='change_recipe'),
    path('registration/', views.registration, name='registration'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('all_recipes/<int:author_id>', views.get_recipes_by_author, name='get_recipes_by_author'),
    path('all_recipes/', views.get_recipes, name='get_recipes'),
    path('add_ingredient/<int:recipe_id>', views.add_ingredient_to_the_recipe, name='add_ingredient'),
    path('delete_ingredient/<int:recipe_id>/<int:info_id>', views.delete_ingredient, name='delete_ingredient'),
]