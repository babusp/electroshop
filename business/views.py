from http.client import responses
from itertools import product
from tabnanny import check
from urllib import request
from django.shortcuts import redirect,render, get_object_or_404,HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics,views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from . import serializers
import stripe

from business.models import (Address, BillingAddress, Coupon, Payment, Product, BusinessProfile,Business,OrderItem,Order, 
                             ShippingAddress, checkout)
from business.serializers import BusinessProfileSerializer,LoginSerializer,AddProductSerializer,LogoutSerializer



from .serializers import (AddProductSerializer, AddressSerializer, BillingAddressSerializer, BusinessSignupSerializer, 
                        CheckoutSerializer,CouponSerializer, OrderSerializer, PaymentSerializer, ShippingAddressSerializer,User)




stripe.api_key = "sk_test_51LauCmSAhFFi8gusJUhPcsTwOJlS4IigHh44rYlpmgVwWMx8PJHAILfuT8h0a3K5mt6L4NECGvVgALhJ0lUIufhR00bLfYVdFh"


# Create your views here.


class LoginAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

class BusinessSignUpAPIView(generics.CreateAPIView):
    permission_classes=(AllowAny,)
    queryset=User.objects.all()
    serializer_class=BusinessSignupSerializer


class BusinessProfileAPIView(generics.CreateAPIView):
    permission_classes=(IsAuthenticated,)
    queryset=BusinessProfile.objects.all()
    serializer_class=BusinessProfileSerializer
  

class ListBusinessProfileAPIView(generics.ListAPIView):
    permission_classes=(IsAdminUser,)
    queryset=BusinessProfile.objects.all()
    serializer_class=BusinessProfileSerializer


class UpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    queryset=BusinessProfile.objects.all()
    serializer_class=BusinessProfileSerializer

class AddProductAPIView(views.APIView):
    permission_classes=(IsAuthenticated,)   
    serializer_class=AddProductSerializer
   
    def post(self, request):
        field_name = 'is_verified'
        obj = Business.objects.first()
        field_value = getattr(obj, field_name)
        if field_value==True:
            serializer=serializers.AddProductSerializer(data=request.data)
            print(serializer)
            print(serializer.is_valid())
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        
        return HttpResponse("profile not verified contact admin")

class ListProductAPIView(generics.ListAPIView) :
    queryset=Product.objects.all()
    serializer_class=AddProductSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=AddProductSerializer



class Add2CartAPIView(views.APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,slug):
        item = get_object_or_404(Product, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
   
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                #return redirect("core:order-summary")
                return HttpResponse("This item quantity was updated.")
            else:
        
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                #return redirect("core:order-summary")
                return HttpResponse("This itemwas added to your cart.")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            #return redirect("core:order-summary")
            return HttpResponse( "This item was added to your cart")



class RemoveFromCartAPIView(views.APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request,slug):
        item = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
                #return redirect("core:order-summary")
                return HttpResponse( "This item was removed to your cart")
            else:
                messages.info(request, "This item was not in your cart")
            #  return redirect("core:product", slug=slug)
                return HttpResponse( "This item was not in your cart")
        else:
            messages.info(request, "You do not have an active order")
            #return redirect("core:product", slug=slug)
            return HttpResponse( "This dont have an active cart")

class CartAPIView(generics.ListAPIView):

    permission_classes=[IsAdminUser,]
    queryset=checkout.objects.all()
    serializer_class=CheckoutSerializer

class AddressCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Address.objects.all()
    serializer_class=AddressSerializer

class AddressCreateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Address.objects.all()
    serializer_class=AddressSerializer



class OrderCreateAPIView(views.APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        # @classmethod
        # def get_total(self):
        #     total = 0
        #     for order_item in self.items.all():
        #         total += order_item.get_final_price()
        #     if self.coupon:
        #         total -= self.coupon.amount
        #     return total
        serializer=CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userid=request.user.id)
            return Response(serializer.data)
        else:
            return Response("not created try again")


class ShippingAddCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=ShippingAddress.objects.all()
    serializer_class=ShippingAddressSerializer


class BillingAddCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=BillingAddress.objects.all()
    serializer_class=BillingAddressSerializer


class ShippingCreateAPIView(views.APIView):

    def post(self,request) :
        serializer=serializers.ShippingAddressSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
            field_name = 'is_billing_address_same'
            obj = ShippingAddress.objects.latest("id")
            field_value = getattr(obj, field_name)
            if field_value == True:
                fields=ShippingAddress.objects.latest("id")
              
                bill=BillingAddress()
                bill.apartment_address=fields.apartment_address
                bill.street_address=fields.street_address
                bill.country=fields.country
                bill.zip=fields.zip
                bill.default=fields.default
                bill.save()
            return Response(serializer.data)


class CouponCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsAdminUser,]
    queryset=Coupon.objects.all()
    serializer_class=CouponSerializer

class CouponListAPIView(generics.ListAPIView):
    permission_classes=[AllowAny,]
    queryset=Coupon.objects.all()
    serializer_class=CouponSerializer


class PaymentCreateListAPIView(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser,]
    queryset=Payment.objects.all()
    serializer_class=PaymentSerializer

class UserCartAPIView(views.APIView):

    permission_classes=[IsAuthenticated,]
        
    def get(self, request):

        queryset=checkout.objects.filter(userid=request.user.id)
        serializer=CheckoutSerializer(queryset,many=True)
        return Response(serializer.data)
     
      
class PaymentAPIView(views.APIView):

    def post(self,request):

        list=checkout.objects.filter(userid=request.user.id)
    
        test_payment_intent = stripe.PaymentIntent.create(
        amount=100, currency='inr', 
        payment_method_types=['card'],
        receipt_email='test@example.com')
        return Response(data=test_payment_intent)

class LogoutView(generics.GenericAPIView):
    """User Logout"""

    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """User Logout validate"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
        












    



    


        