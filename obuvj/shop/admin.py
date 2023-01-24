from django.contrib import admin

# Register your models here.
from shop.models import Payment,Product, OrderItem, Order

admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)