FROM python:3.8.9-slim-buster

# UPDATE/UPGRADE PACKAGES, INSTALL PIP, PING, TZ
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install iputils-ping -y \
    && apt-get install tzdata -y \
    && pip3 install --upgrade pip

# INSTALL REQUIREMENTS
COPY requirements.txt /
RUN pip3 install -r requirements.txt

# CREATE APP DIR, MAKE IT A WORKDIR
RUN mkdir app
WORKDIR /app
