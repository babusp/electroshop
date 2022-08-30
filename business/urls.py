from django.urls import path
from business.views import (Add2CartAPIView, AddProductAPIView, AddressCreateAPIView, BillingAddCreateAPIView, CartAPIView, CouponCreateAPIView, CouponListAPIView,ListProductAPIView, BusinessProfileAPIView, 
                    BusinessSignUpAPIView,LoginAPIView,ListBusinessProfileAPIView, OrderCreateAPIView, PaymentAPIView, PaymentCreateListAPIView, ProductDetailAPIView, 
                    RemoveFromCartAPIView, ShippingAddCreateAPIView, ShippingCreateAPIView,UpdateDeleteAPIView, 
                    UserCartAPIView,LogoutView)
from rest_framework_simplejwt.views import TokenRefreshView




urlpatterns=[

    path("login/",LoginAPIView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),

    path("signup/",BusinessSignUpAPIView.as_view()),
    path("profile/",BusinessProfileAPIView.as_view()),
    path("list/",ListBusinessProfileAPIView.as_view()),
    path('rudop/<int:pk>/',UpdateDeleteAPIView.as_view()),
    path("addproduct/",AddProductAPIView.as_view()),
    path("listproduct/",ListProductAPIView.as_view()),
    path("productdetail/<int:pk>/",ProductDetailAPIView.as_view()),
    path("add2cart/<slug>/",Add2CartAPIView.as_view()),
    path("cart/",CartAPIView.as_view()),
    path("ucart/",UserCartAPIView.as_view()),
    path("removecart/<slug>/",RemoveFromCartAPIView.as_view()),
    path("addaddress/",AddressCreateAPIView.as_view()),
    path("ordercreate/",OrderCreateAPIView.as_view()),
    path("shipping/",ShippingAddCreateAPIView.as_view()),
    path("billing/",BillingAddCreateAPIView.as_view()),
    path("sh/",ShippingCreateAPIView.as_view()),
    path("couponadd/",CouponCreateAPIView.as_view()),
    path("couponlist/",CouponListAPIView.as_view()),
    path("paymode/",PaymentCreateListAPIView.as_view()),
    path("pay/",PaymentAPIView.as_view()),
     path("logout/", LogoutView.as_view(), name="logout"),

    


    
    


]




