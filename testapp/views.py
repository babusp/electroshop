from http.client import responses
from django.shortcuts import render
from rest_framework import generics,views
from testapp.models import UserProfile
# from .models import User, UserProfile
from testapp.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
class UserProfileAPIView(views.APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request):
        print(request.user.id,"=======================")
        serializer=UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userid=request.user.id)
            return Response(serializer.data)
        else:
            return Response("not created try again")


  
           
    def get(self,request):
        
        logid=str(request.user.id)
        queryset=UserProfile.objects.filter(userid=logid)
        serializer=UserProfileSerializer(queryset,many=True)
        return Response(serializer.data)

    
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
class sendotpview(views.APIView):
    def post(self,request):       
        print("------------------------")  
        account_sid = "ACxxxxxxxxxxxxxxxxxxxxxxxxxx"
        auth_token ='2dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                                    from_='+1555xxxxxxx',
                                    body='Hi there',
                                    to='+918121xxxxxxx'
                                )

        print(message.sid)
