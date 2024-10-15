from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User     

# Register your models here.
# @admin.register(ChatGroup)
# class GroupAdmin(admin.ModelAdmin):
#     list_diplay = ['name', 'creator', 'description']
#     search_fields = ['name', 'creator__username']


# @admin.register(ChatGroupMembers)
# class GroupMemberAdmin(admin.ModelAdmin):
#     list_display = ['group', 'members', 'role']
#     search_fields = ['group__name', 'members__username']
#     list_filter = ['role']


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['phone_number', 'username']
    search_fields = ['username', 'phone_number']
