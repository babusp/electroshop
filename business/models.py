
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django. utils import  timezone


# Create your models here.

class BusinessProfile(models.Model):
    title=models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    phone_no = models.CharField(unique=True, max_length=17, null=True, blank=True)
    business_name=models.CharField(max_length=100)
    business_type=models.CharField(max_length=100)
    business_id=models.CharField(max_length=100,unique=True)
    location=models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
   



class AddProduct(models.Model):
    product_type=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    image=models.ImageField(null=True, blank=True)

class Business(models.Model):
    title=models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    phone_no = models.CharField(unique=True, max_length=17, null=True, blank=True)
    business_name=models.CharField(max_length=100)
    business_type=models.CharField(max_length=100)
    business_id=models.CharField(max_length=100,unique=True)
    location=models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title




class Product(models.Model):
    product_name=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    image=models.ImageField(null=True, blank=True)
    business=models.ForeignKey(Business,on_delete=models.CASCADE)
    slug=models.SlugField()

    def __str__(self):
        return self.product_name

    # class Meta:
    #     ordering = ['product_type']




class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.product_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()



ADDRESS_CHOICES = (
    ('Billing_Address', 'Billing'),
    ('Shipping_Address', 'Shipping'),
)



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=30, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.CASCADE, blank=True, null=True)
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class ShippingAddress(models.Model):
    apartment_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    is_billing_address_same=models.BooleanField(default=False)

    def __str__(self):
        return self.apartment_address + " " + self.street_address

    class Meta:
        verbose_name_plural = 'ShippingAddresses'

class BillingAddress(models.Model):
    apartment_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.apartment_address

    class Meta:
        verbose_name_plural = 'BillingAddresses'



# class Payment(models.Model):
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username
class Payment(models.Model):
    method=models.CharField(max_length=50)
    
    def __str__(self):
        return self.method




class Coupon(models.Model):
    code= models.CharField(max_length=150)

    def __str__(self):
        return self.code





class checkout(models.Model):
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(default=timezone.now())
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        ShippingAddress, related_name='shipping_address', on_delete=models.CASCADE, blank=True, null=True)
    billing_address = models.ForeignKey(
        BillingAddress, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    userid=models.CharField(max_length=15)
    
    
    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        
        return self.userid

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

