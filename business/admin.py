from itertools import product
from django.contrib import admin

from business.models import Address, BillingAddress, Coupon, Order,AddProduct, Business, BusinessProfile, OrderItem, Payment,Product, Refund, ShippingAddress, checkout

# Register your models here.
admin.site.register(BusinessProfile)
admin.site.register(AddProduct)
admin.site.register(Business)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(checkout)