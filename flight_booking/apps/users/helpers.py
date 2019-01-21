import jwt
import os

from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from random import randint, choice

from .models import User
from .serializers import UserSerializer
from .auth import VerifyToken


def handle_validate_and_update_user(request, validated_user_data, id=None):
    """It handles validate and update user details

    :param request: contains request data
    :param validated_user_data: contains validated user data
    :param id: user id
    :return: response message
    """
    if validated_user_data.is_valid():
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        user.phone_number = request.data.get('phone_number') if request.data.get(
            'phone_number') else user.phone_number
        user.first_name = request.data.get('first_name') if request.data.get('first_name') else user.first_name
        user.last_name = request.data.get('last_name') if request.data.get('last_name') else user.last_name
        user.save()
        user = UserSerializer(user).data
        return Response({'message': 'Details updated successfully.', 'data': user}, status=status.HTTP_200_OK)
    return Response({'message': validated_user_data.errors}, status=status.HTTP_400_BAD_REQUEST)


def handle_admin_user_check(request):
    authenticated_user, none_value = VerifyToken().authenticate(request)
    if authenticated_user.is_superuser:
        return True
    elif not authenticated_user or not str(authenticated_user.id) in request.path:
        raise exceptions.AuthenticationFailed('Sorry, you do not have the permission')
    return True


def generate_token(email, token_expire_date):
    """
    It generates user token
    :param email: user email
    :param token_expire_date: time taken for token to expire
    :return: token
    """
    token = jwt.encode({'email': email,
                        'exp': token_expire_date},
                       os.getenv('APP_SECRET_KEY'), algorithm='HS256')
    return token


def generate_random_pass_key():
    """
    It generates random pass key
    :return: randomly generated values
    """
    rand_number = f'{randint(1, 9999999999)}'
    rand_char = choice('@#&*$%')
    rand_small_letter = choice('abcdefghij')
    rand_cap_letter = choice('AFBHRQ')
    return rand_number+rand_cap_letter+rand_char+rand_small_letter
