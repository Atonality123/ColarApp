from django.contrib import admin
from .models import User

class MemberAdmin(admin.ModelAdmin):
  list_display = ("username", "password")
  
admin.site.register(User, MemberAdmin)