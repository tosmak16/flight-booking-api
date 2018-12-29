from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
import jwt, os
from datetime import datetime, timedelta


from django.contrib.auth import authenticate



class UserDetailViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            instance = serialized_user.save()
            instance.set_password(instance.password)
            instance.save()
            return Response(data=serialized_user.data, status=status.HTTP_201_CREATED)
        return Response({'message': serialized_user.errors}, status=status.HTTP_400_BAD_REQUEST)