from django.contrib import admin

# Register your models here.

from .models import product, subuser, order

admin.site.register(product)
admin.site.register(subuser)
admin.site.register(order)