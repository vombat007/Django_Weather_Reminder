# DjangoWeatherReminder

# Introduction:

A Django REST framework-powered web application offers a weather notification service.

The Weather Reminder application supplies an API for accessing weather-related information.

This application boasts the following functionalities:

- Upon registration, clients receive a unique API key to gain future access to the application.
- Following login, clients are issued a JWT token.
- Users can subscribe to weather notifications through the REST API. They can select cities and specify the frequency of
  notifications (1, 3, 6, or 12 hours).
- Users have the ability to add, update, or delete cities in their subscription, modify the notification frequency, and
  cancel their subscription via the REST API.
- The Weather Reminder app utilizes the OpenWeather API service (https://openweathermap.org/api) to retrieve up-to-date
  weather data.
- Users receive notifications via email at the specified intervals mentioned in their subscription. This functionality
  is implemented using Redis, Celery Beat, asynchronous periodic tasks, and SendGrid.
- Users can request current weather information for cities in their subscription at any time and receive a
  JSON-formatted response via the REST API.
- The application is packaged within a Docker container.

Unit tests have been implemented to ensure the application's functionality and reliability.

____

## Getting started

## Docker
## Use to build docker images

```commandline
docker build -t weather_reminder_docker .
```
## Use to run or stop docker container
```commandline
docker compose up
docker compos down
```
## Documentation by Swagger
### See url of documentation
~~~ 
http://your_ip/api/docs/

http://your_ip/api/schema/
~~~


## Use to fill database:

### 1 = {number_of_users},2 = {number_of_cities},3 = {number_of_subscriptions}

```commandline
python manage.py populane_db 1 2 3 --settings=weather_reminder.settings.dev

or

python manage.py populane_db 1 2 3 --settings=weather_reminder.settings.prod
```

## Run the app locally :

```commandline
python manage.py runserver --settings=weather_reminder.settings.dev
```

# CELERY

### For run celery worker and schedule on windows use this command

```commandline
celery -A weather_reminder worker -P eventlet -l INFO
celery -A weather_reminder beat --loglevel=INFO 
```

# Unit tests

## To run tests use this command:

```commandline
python manage.py test reminder.tests.tests_views --settings=weather_reminder.settings.dev
python manage.py test reminder.tests.tests_model --settings=weather_reminder.settings.dev
```

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file)
  or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line)
  or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin http://git.foxminded.ua/foxstudent103147/task-17-create-basic-application.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](http://git.foxminded.ua/foxstudent103147/task-17-create-basic-application/-/settings/integrations)
