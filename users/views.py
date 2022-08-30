from django.shortcuts import render
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from .serializers import ListSerializer, LoginSerializer, SignupSerializer
from .serializers import User

# Create your views here.
class LoginAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

class SignupAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset=User.objects.all()
    serializer_class=SignupSerializer

class ListAPIView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset=User.objects.all()
    serializer_class=SignupSerializer

class UpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    queryset=User.objects.all()
    serializer_class=ListSerializer

    
