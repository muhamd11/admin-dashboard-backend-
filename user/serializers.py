from django.conf import settings
from django.forms import ValidationError
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes
from django.urls import reverse


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'is_staff', 'is_active',
                  'date_joined', 'first_name', 'last_name', 'mobile', 'email', 'image', 'groups', 'user_permissions']
        
    def get_image(self, obj):
        if hasattr(obj, 'image') and obj.image:
            # Assuming obj.image contains the path to the image
            base_url = settings.MEDIA_URL
            return self.context['request'].build_absolute_uri(f"{base_url}{obj.image}")
        return None
    
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'mobile']  

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise ValueError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'mobile']  



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6, write_only=True)
    password = serializers.CharField(min_length=6, write_only=True)
    access_token = serializers.CharField(max_length=68, read_only=True)
    refresh_token = serializers.CharField(max_length=68, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token', 'user']
        

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get("password")
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials. Please try again.')

        user_token = user.tokens()

        # Construct the response dictionary with user object and other required fields
        response_data = {
            'user': UserSerializer(user, context=self.context).data,
            'access_token': str(user_token.get('access')),
            'refresh_token': str(user_token.get('refresh')),
        }

        return response_data