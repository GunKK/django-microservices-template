# pull official base image
FROM python:3.10-slim

ENV APP_HOME=/usr/src/service
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/app
RUN mkdir $APP_HOME/core
RUN mkdir $APP_HOME/apis

# set work directory
WORKDIR /usr/src/service

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=False
ENV TZ=Asia/Ho_Chi_Minh

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    unixodbc-dev \
    gnupg2 \
    apt-transport-https \
    vim \
    tzdata \
    pkg-config \
    netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Add Microsoft’s APT repository for ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-prod.list \
    && apt-get update

# Install the Microsoft ODBC Driver 17 for SQL Server
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# install dependencies
RUN pip install -U pip poetry && \
    rm -rf /root/.cache/pip
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install

# copy folder
COPY . $APP_HOME

