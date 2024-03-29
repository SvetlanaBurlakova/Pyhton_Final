from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Recipe, Ingredient, Category,IngredientInfo


# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ['firstname', 'lastname']
#     ordering = ['lastname']
#     list_filter = ['lastname']
#     search_fields = ['lastname']
#     search_help_text = 'Поиск по полю фамилия автора'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_type']
    ordering = ['name']
    list_filter = ['name']
    search_fields = ['name']
    search_help_text = 'Поиск по полю название ингредиента'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    ordering = ['name']
    list_filter = ['name']
    search_fields = ['name']
    search_help_text = 'Поиск по полю название категории'


class IngredientInfoAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'count']
    ordering = ['ingredient']
    list_filter = ['ingredient']
    search_fields = ['ingredient']
    search_help_text = 'Поиск по полю название ингредиента'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'steps', 'cooking_time', 'image']
    ordering = ['name']
    list_filter = ['name']
    search_fields = ['name']
    search_help_text = 'Поиск по полю название рецепта'



# Register your models here.
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInfo, IngredientInfoAdmin)
# admin.site.register(Author, AuthorAdmin)