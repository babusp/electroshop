from urllib import request
from rest_framework import serializers
from .models import UserProfile




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=["firstname","lastname","email","phone","userid"]
        extra_kwargs = {'userid': {'read_only':True}}


        # def create(self,validated_data):
        #     print("------------------")
        #     print(request.user.id)
        #     user = UserProfile.objects.create(
        #     firstname=validated_data["firstname"],
        #     lastname=validated_data["lastname"],
        #     email=validated_data["email"],
        #     phone=validated_data["phone"],
        #     userid=request.user.id
        #     )
        #     user.save()



        


