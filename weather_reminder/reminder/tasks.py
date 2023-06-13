from collections import defaultdict
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from reminder.utils import send_weather_email, fetch_weather_data
from .models import Weather, Subscription
from datetime import timedelta


@shared_task()
def send_weather_notifications():
    current_time = timezone.now()
    fetch_weather_data()

    subscriptions = Subscription.objects.select_related('user', 'city')

    user_weather_data = defaultdict(list)

    for subscription in subscriptions:
        user = subscription.user
        city = subscription.city

        try:
            latest_weather = Weather.objects.filter(city=city).latest('timestamp')
            weather_info = f"Temperature: {latest_weather.temperature}, " \
                           f"Conditions: {latest_weather.weather_conditions}, " \
                           f"Feels Like: {latest_weather.feels_like}"

            last_notification_sent = subscription.last_notification_sent
            last_weather_request = city.last_weather_request

            if last_notification_sent is None or (
                    current_time - last_notification_sent) >= timedelta(hours=subscription.period):
                if last_weather_request is None or (
                        current_time - last_weather_request) >= timedelta(hours=subscription.period):
                    user_weather_data[user].append((city, weather_info))
                    subscription.last_notification_sent = current_time
                    city.last_weather_request = current_time
                    subscription.save()
                    city.save()

        except ObjectDoesNotExist:
            print(f"No weather data found for city: {city}")

    for user, city_weather_data in user_weather_data.items():
        cities = set()
        filtered_city_weather_data = []

        for city, weather_info in city_weather_data:
            if city not in cities:
                filtered_city_weather_data.append((city, weather_info))
                cities.add(city)

        if filtered_city_weather_data:
            send_weather_email(user, filtered_city_weather_data)
            print('Email sent')
