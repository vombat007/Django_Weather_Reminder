from django.urls import path
from . import views
from .views import RegisterView, CityListCreateView, SubscriptionListCreateView
from .views import SubscriptionRetrieveUpdateDestroyView, GitHubRegistrationAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/registration/', views.registration, name='registration'),
    path('api/registration/github/', GitHubRegistrationAPIView.as_view(), name='github-registration'),

    path('api/cities/', CityListCreateView.as_view(), name='cities'),
    path('api/subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('api/subscription/<int:pk>/', SubscriptionRetrieveUpdateDestroyView.as_view(),
         name='subscription-retrieve-update-destroy'),

    # Swagger URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
