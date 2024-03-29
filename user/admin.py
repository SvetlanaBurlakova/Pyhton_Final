from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    ordering = ['last_name']
    list_filter = ['last_name']
    search_fields = ['last_name']
    search_help_text = 'Поиск по полю фамилия автора'


admin.site.register(User, UserAdmin)