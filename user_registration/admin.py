from django.contrib import admin
from .models import CustomUser
# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name') 

    
admin.site.register(CustomUser, UserProfileAdmin)

