from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer


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
        return Response({'message': 'Details updated successfully', 'data': user}, status=status.HTTP_200_OK)
    return Response({'message': validated_user_data.errors}, status=status.HTTP_400_BAD_REQUEST)
