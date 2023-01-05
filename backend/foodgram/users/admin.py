from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Follow, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'first_name')


@admin.register(Follow)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
