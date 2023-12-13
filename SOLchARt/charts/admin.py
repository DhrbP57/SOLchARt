from django.contrib import admin
from .models import Member, Data

# Register your models here.
admin.site.register(Member)

class DataAdmin(admin.ModelAdmin):
    list_filter = ('user', 'date')

admin.site.register(Data, DataAdmin)