from django.contrib import admin

# Register your models here.
from .models import Users, UsersCustomers, CustomerInvoicer

admin.site.register(Users)
admin.site.register(UsersCustomers)
admin.site.register(CustomerInvoicer)
