from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile 

# Unregister Groups
admin.site.unregister(Group)

# Mix profile info into User info in admin
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

# Unregister initial user
admin.site.unregister(User)

# Re-register User
admin.site.register(User, UserAdmin)

