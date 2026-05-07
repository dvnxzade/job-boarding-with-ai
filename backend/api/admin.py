from .models import Category , User , Job , Application
from django.contrib import admin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("email" , "first_name" , "last_name")

class JobAdmin(admin.ModelAdmin):
    list_display = ("title" , "category" , "company_name" , "is_active")

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job" , "cover_letter" , "status" , "applied_at" , "relevancy_score")

admin.site.register(Category)
admin.site.register(User , UserAdmin)
admin.site.register(Job , JobAdmin)
admin.site.register(Application , ApplicationAdmin)
