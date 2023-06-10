from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reminder.models import User, City, Subscription


class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_github_registration_api_view(self):
        url = reverse('github-registration')
        data = {'github_email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_view(self):
        url = reverse('register')
        data = {
            'email': 'test1@example.com',
            'password': 'testpassword',
            # Include other required fields for UserSerializer
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_city_list_create_view(self):
        url = reverse('cities')
        data = {'name': 'London'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_list_create_view(self):
        city = City.objects.create(name='Kiev')
        url = reverse('subscription-list-create')
        data = {
            'user': self.user.pk,
            'city': city.pk,
            'period': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_retrieve_update_destroy_view(self):
        user = User.objects.create_user(email='test4@example.com', password='testpassword')
        city = City.objects.create(name='Berlin')
        subscription = Subscription.objects.create(user=user, city=city, period=1)

        # Authenticate the client
        self.client.force_authenticate(user=user)

        url = reverse('subscription-retrieve-update-destroy', kwargs={'pk': subscription.pk})
        data = {
            'user': user.pk,
            'city': city.pk,
            'period': 3,  # Update the period
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
