from django.shortcuts import render
from rest_framework import decorators,response,status
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from . import models
# Create your views here.


@decorators.api_view(["POST",])
def logOut(request):
    if request.method == "POST":
       request.user.auth_token.delete()
       return response.Response(status=status.HTTP_200_OK)

@decorators.api_view(["POST",])
def registeration_view(r):
    if r.method == "POST":
        serializer = RegistrationSerializer(data=r.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data["response"] = "successfully registered new user."
            data["username"] = account.username
            data["email"] = account.email
            token=Token.objects.get(user=account).key
            data["token"] = token
            # return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data= serializer.errors
            # return response.Response(data, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(data)
            