from django.contrib import admin

# Register your models here.
from app_user import models

admin.site.register(models.User)
admin.site.register(models.CurrentUser)