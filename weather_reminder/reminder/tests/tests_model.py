from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from reminder.models import City, Subscription, Weather

User = get_user_model()


class ModelTests(TestCase):

    def setUp(self):
        self.city = City.objects.create(name='Test City')
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.subscription = Subscription.objects.create(user=self.user, city=self.city, period=1)

    def test_city_creation(self):
        city_count = City.objects.count()
        self.assertEqual(city_count, 1)

    def test_subscription_creation(self):
        subscription_count = Subscription.objects.count()
        self.assertEqual(subscription_count, 1)

    def test_weather_creation(self):
        weather = Weather.objects.create(
            city=self.city,
            temperature=25.5,
            weather_conditions='Sunny',
            feels_like=27.0,
            timestamp='2023-06-02 12:00:00')
        weather_count = Weather.objects.count()
        self.assertEqual(weather_count, 1)

    def test_user_creation(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_unique_city_name(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name='Test City')

    def test_subscription_user_relationship(self):
        subscription = Subscription.objects.get(id=self.subscription.id)
        self.assertEqual(subscription.user, self.user)

    def test_subscription_city_relationship(self):
        subscription = Subscription.objects.get(id=self.subscription.id)
        self.assertEqual(subscription.city, self.city)
