import jwt, os
from django.contrib.auth.models import User
from .models import User
from rest_framework import authentication, exceptions


class VerifyToken(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN') or request.META.get('token')
        if token is None:
            raise exceptions.AuthenticationFailed('Token is required.')
        key = os.getenv('APP_SECRET_KEY')
        email = None
        try:
            email = jwt.decode(token, key=key, algorithms=['HS256'], options={
                        'verify_signature': True,
                        'verify_exp': True

            }).get('email')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidAlgorithmError as error:
            if str(error):
                raise exceptions.AuthenticationFailed('User Authorization failed. Enter a valid token.')
        except jwt.DecodeError as error:
            if str(error) == 'Signature verification failed':
                raise exceptions.AuthenticationFailed('Token Signature verification failed.')
            else:
                raise exceptions.AuthenticationFailed('Authorization failed due to an Invalid token.')

        if not email:
            return email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user.')
        return user, None

