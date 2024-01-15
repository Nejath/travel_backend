from rest_framework import serializers
from .models import CustomUser,Package,Comments,Blogs
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # adding custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["is_superuser"] = user.is_superuser
        data["username"] = user.username
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'place', 'nickname', 'color', 'image', 'password','password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        try:
            CustomUser.objects.get(email=data['email'])
            raise serializers.ValidationError({'email':'Email already exists.'})
        except ObjectDoesNotExist:
            pass

        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop({'password_confirmation ':'password_confirmation'}, None)
        user = CustomUser.objects.create_user(**validated_data)

        return user


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        exclude = ['admin']

class PackagelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['comment']

class CommentlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        exclude = ['user']

class BloglistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = "__all__"
