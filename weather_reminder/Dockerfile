FROM python:3.11.3

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

Run apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim


RUN useradd -rms /bin/bash reminder && chmod 777 /opt /run

WORKDIR /weather_reminder

COPY --chown=weather_reminder:weather_reminder . .

RUN pip install -r requirements.txt

USER reminder


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--env DJANGO_SETTINGS_MODULE=weather_reminder.settings.prod weather_reminder.wsgi:application"]
