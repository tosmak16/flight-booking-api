from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from datetime import datetime

from .serializers import UserSerializer, UserUpdateSerializer
from .models import User
from .permissions import PatchAdminAndUserPermissions, PutAdminAndUserPermissions, GetAdminAndUserPermissions
from ...config.settings import TOKEN_EXP
from .helpers import handle_validate_and_update_user, generate_token, generate_random_pass_key, send_password_reset_email
from flight_booking.utils.backgroundWorker import BackgroundTaskWorker


class UserDetailViewSet(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin):
    """ It handles user operations like sign up, sign in, update, retrieve """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (PatchAdminAndUserPermissions,
                          GetAdminAndUserPermissions,
                          PutAdminAndUserPermissions,
                          )
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
            return Response({'message': 'email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'message': 'password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'message': 'email or password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        token_exp_date = datetime.now() + TOKEN_EXP
        token = generate_token(user.email, token_exp_date)
        return Response({'message': 'you have logged in successfully', 'token': token}, status=status_type)

    @action(methods=['PATCH', 'DELETE'], detail=True)
    def passport(self, request, id):
        passport = request.data.get('passport')
        if passport is None or len(str(passport).strip()) is 0 and request.method == "PATCH":
            return Response({'message': 'passport field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        user.passport_url.delete()
        if request.method == "PATCH":
            user.passport_url = passport
            user.save()
            return Response({'message': 'Passport updated successfully.'}, status=status.HTTP_200_OK)
        user.save()
        return Response({'message': 'Passport deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, id=None, *args, **kwargs):
        """It updates user details

        :param request: contains request data
        :param id: user id
        :param args:
        :param kwargs
        :return: response message or data
        """
        validated_user_data = UserUpdateSerializer(data=request.data)
        return handle_validate_and_update_user(request, validated_user_data, id)

    def partial_update(self, request, id=None, *args, **kwargs):
        """It partially updates user details

        :param request: contains request data
        :param id: user id
        :param args:
        :param kwargs
        :return: response message or data
        """
        validated_user_data = UserSerializer(data=request.data, partial=True)
        return handle_validate_and_update_user(request, validated_user_data, id)

    @action(methods=['POST'], detail=False)
    def password(self, request):
        """
        It handles new user creation
        :param request:
        :return:  success message or error message
        """
        email = request.data.get('email')
        new_password = generate_random_pass_key()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Account does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(new_password)
        user.save()
        BackgroundTaskWorker.start_work(send_password_reset_email, (user, new_password))
        return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)

