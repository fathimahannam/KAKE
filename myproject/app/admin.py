from django.contrib import admin
from .models import *
from .models import UserAccount

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Transaction)
admin.site.register(Address)