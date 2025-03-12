from django.contrib import admin

# Register your models here.
from .models import customer,Booking,Contact
admin.site.register([customer,Booking,Contact])