import random
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker
from reminder.models import City, Subscription, User
import randomname
from reminder.utils import get_weather_data


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', type=int, help='Number of fake users to create')
        parser.add_argument('number_of_cities', type=int, help='Number of fake cities to create')
        parser.add_argument('number_of_subscriptions', type=int, help='Number of fake subscriptions to create')

    def handle(self, *args, **options):
        number_of_users = options['number_of_users']
        number_of_cities = options['number_of_cities']
        number_of_subscriptions = options['number_of_subscriptions']

        fake = Faker()

        for i in range(number_of_users):
            email = fake.email()[:30]
            password = make_password(fake.password())[:30]

            user = User(email=email, password=password)
            user.save()

        for _ in range(number_of_cities):
            while True:
                name = randomname.generate('names/cities/')
                if get_weather_data(name) == 404:
                    continue
                else:
                    City.objects.create(name=name)
                    print(f"City created: {name}")
                    break

        users = User.objects.all()
        cities = City.objects.all()
        periods = [1, 3, 6, 12]
        for _ in range(number_of_subscriptions):
            user = random.choice(users)
            city = random.choice(cities)
            period = random.choice(periods)  # Random period from the available options
            Subscription.objects.create(user=user, city=city, period=period)
            print(f"Subscription created: {user.email} - {city.name}")

        self.stdout.write(self.style.SUCCESS(
            f'Successfully populated the database with {number_of_users} users, '
            f'{number_of_cities} cities, '
            f'{number_of_subscriptions} users subscriptions, and ')
        )
