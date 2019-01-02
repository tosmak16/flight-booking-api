import re
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer
    """
    password = serializers.CharField(
        write_only=True,
        min_length=9,
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'passport_url')

    @staticmethod
    def validate_password(password):
        """
        Validates password
        :param password:
        :return: password
        """

        if re.search(r'(^(?=.*[a-z].*[a-z])(?=.*[A-Z].*[A-Z'
                     r'])(?=.*\d.*\d)(?=.*\W.*\W)[a-zA-Z0-9\S]{9,}$)', password) is not None:
            return password
        raise serializers.ValidationError(
            'Password value should have at least 2 uppercase, 2 lowercase, 2 digit and 2 special character.'
        )
        
    @staticmethod
    def validate_email(email):
        """
        Validates email
        :param email:
        :return: email
        """
        if re.search(r'(^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]'
                     r'{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$)', email) is not None:
            return email
        raise serializers.ValidationError(
            'Enter a valid email address.'
        )