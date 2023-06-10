from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, City, Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    last_notification_sent = serializers.DateTimeField(read_only=True, default=None)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'city', 'period', 'last_notification_sent']


class GitHubRegistrationSerializer(serializers.Serializer):
    github_email = serializers.EmailField()

    def create(self, validated_data):
        github_user = get_user_model()
        github_email = validated_data.get('github_email')
        user, created = github_user.objects.get_or_create(email=github_email)
        return user
