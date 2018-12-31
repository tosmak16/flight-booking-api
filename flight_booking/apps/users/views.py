import jwt
import os

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from datetime import datetime

from .serializers import UserSerializer
from .models import User
from .permissions import IsAdmin, IsOwner, PatchAdminAndUserPermissions
from ...config.settings import TOKEN_EXP


class UserDetailViewSet(viewsets.GenericViewSet):
    
    """ It handles user operations like sign up, sign in, update, retrieve """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner, PatchAdminAndUserPermissions, )
    lookup_field = 'id'

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        """
        It handles new user creation
        :param request:
        :return:  success message or error message
        """
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            instance = serialized_user.save()
            instance.set_password(instance.password)
            instance.save()
            return self.signin(request, status.HTTP_201_CREATED)
        return Response({'message': serialized_user.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def signin(self, request, status_type=status.HTTP_200_OK):

        """
        It handles user sign in
        :param request:
        :param status_type: string
        :return: success message or error message
        """
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return Response({'message': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'message': 'password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'message': 'email and password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        token = jwt.encode({'email': user.email,
                            'exp': datetime.utcnow() + TOKEN_EXP},
                           os.getenv('APP_SECRET_KEY'), algorithm='HS256')
        return Response({'message': 'you have logged in successfully', 'token': token}, status=status_type)

    @action(methods=['PATCH', 'DELETE'], detail=True)
    def passport(self, request, id):
        passport = request.data.get('passport')
        if passport is None or len(str(passport).strip()) is 0 and request.method is "PATCH":
            return Response({'message': 'passport field is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        user.passport_url.delete()
        if request.method is "PATCH":
            user.passport_url = passport
            user.save()
            return Response({'message': 'Passport Updated successfully'}, status=status.HTTP_200_OK)
        user.save()
        return Response({'message': 'Passport deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
