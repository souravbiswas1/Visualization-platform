FROM python:3.6-alpine
# Install required packages
RUN apk add --update --no-cache \
    build-base \
    postgresql-dev \
    linux-headers \
    pcre-dev \
    py-pip \
    bash \
    curl \
    openssl \
    nginx \
    libressl-dev \
    musl-dev \
    libffi-dev \
    rsyslog

RUN pip install --upgrade pip
RUN pip install Cython

RUN mkdir -p /Visualization-Docker
COPY requirements.txt /Visualization-Docker
RUN pip install -r /Visualization-Docker/requirements.txt
COPY ./ /Visualization-Docker
WORKDIR /Visualization-Docker

RUN chmod +x manage.py
EXPOSE 8000
CMD ./manage.py migrate --noinput && ./manage.py runserver 0.0.0.0:8000
