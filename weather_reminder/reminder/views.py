from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import City, Subscription
from .serializers import UserSerializer, CitySerializer, SubscriptionSerializer, GitHubRegistrationSerializer
from rest_framework.response import Response
from .utils import get_weather_data, generate_jwt_token


class GitHubRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GitHubRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        github_email = serializer.validated_data.get('github_email')
        user_in_db = get_user_model()

        try:
            user = user_in_db.objects.get(email=github_email)
        except user_in_db.DoesNotExist:
            return Response({'detail': 'Email wrong or not registered with GitHub'},
                            status=status.HTTP_400_BAD_REQUEST)

        token = generate_jwt_token(user)
        return Response(token)


# view for registering users
class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt_token(user)
            return Response(token)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def registration(request):
    return render(request, 'social/registration.html')


class CityListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def create(self, request, *args, **kwargs):
        city_name = request.data.get('name')

        if get_weather_data(city_name) == 404:
            return Response(
                {'detail': 'You input wrong city or city do not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)


class SubscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        city_id = request.data.get('city')
        period = request.data.get('period')

        # Check if the user already has a subscription for the given city and period
        existing_subscription = Subscription.objects.filter(user=user, city_id=city_id, period=period).exists()
        if existing_subscription:
            return Response(
                {'detail': 'You are already subscribed to this city within the same period.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Associate the logged-in user with the subscription
        request.data['user'] = user.id

        return super().create(request, *args, **kwargs)


class SubscriptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied()
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
