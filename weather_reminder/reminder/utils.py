import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Weather, Subscription
from weather_reminder.settings.base import env


def get_weather_data(city_name):
    api_key = env("OPEN_WEATHER_API_KEY")
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def send_weather_email(user, city_weather_data):
    subject = 'Weather Notification'
    html_message = render_to_string(
        'social/weather.html',
        {'user': user, 'city_weather_data': city_weather_data})

    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message,
              'Weather_Reminder <vombat007@gmail.com>',
              [user.email], html_message=html_message)


def fetch_weather_data():
    subscriptions = Subscription.objects.all()
    processed_cities = set()

    for subscription in subscriptions:
        city = subscription.city

        if city in processed_cities:
            continue

        weather_data = get_weather_data(city.name)
        if weather_data:
            temperature = weather_data['main']['temp']
            weather_conditions = weather_data['weather'][0]['description']
            feels_like = weather_data['main']['feels_like']
            timestamp = timezone.now()

            Weather.objects.create(
                city=city,
                temperature=round(temperature, 1),
                weather_conditions=weather_conditions,
                feels_like=round(feels_like, 1),
                timestamp=timestamp
            )

            processed_cities.add(city)

    print('Weather data successfully fetched and stored')


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return token
