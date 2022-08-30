
from dataclasses import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

from business.models import BillingAddress, Business, Coupon, Order, Payment,Product,Address, ShippingAddress, checkout



class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class BusinessSignupSerializer(serializers.ModelSerializer): 

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email',)
      

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Business
        fields="__all__"
        extra_kwargs = {'is_verified': {'read_only':True}}
        

class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model=checkout
        fields=["userid","items","shipping_address","billing_address","payment","coupon"]
        extra_kwargs={"userid":{"read_only":True}}

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields="__all__"
class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillingAddress
        fields="__all__"
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"
    

class LogoutSerializer(serializers.Serializer):
    """User LogoutSerializer"""

    refresh = serializers.CharField()

    def validate(self, attrs):
        """User LogoutSerializer"""
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        """User Logout Exception handling"""
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError("No Logged in User.")

        