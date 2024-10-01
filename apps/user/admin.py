from django.contrib import admin
from .models import User, Group, GroupMembers     

# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_diplay = ['name', 'creator', 'description']
    search_fields = ['name', 'creator__username']


@admin.register(GroupMembers)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['group', 'user', 'role']
    search_fields = ['group__name', 'user__username']
    list_filter = ['role']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'username']
    search_fields = ['username', 'phone_number']
