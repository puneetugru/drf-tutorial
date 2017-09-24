from .models import Product, Review
from rest_framework import serializers

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class AuthSerializerMixin(object):
    def restore_object(self, attrs, instance=None):
        if attrs.get("username", None):
            attrs["username"] = attrs["username"].lower()
        if attrs.get("email", None):
            attrs["email"] = attrs["email"].lower()
        if attrs.get("password", None):
            attrs["password"] = make_password(base64.decodestring(attrs["password"]))
            

class ReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Review
        fields = ('id', 'title', 'review', 'rating', 'created_by')


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'reviews')


class LoginSerializer(AuthSerializerMixin, serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField('get_client_id')
    client_secret = serializers.SerializerMethodField('get_client_secret')

    class Meta:
        model = User
        fields = ('client_id', 'client_secret')

    def get_client_id(self, obj):
        return obj.application_set.first().client_id

    def get_client_secret(self, obj):
        return obj.application_set.first().client_secret


class SocialSignUpSerializer(LoginSerializer):
    class Meta(LoginSerializer.Meta):
        fields = ('email', 'username', 'client_id', 'client_secret')
        read_only_fields = ('username',)