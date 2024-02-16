FROM python:3.9.6-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update \
    && apt-get install -y build-essential python3-dev default-libmysqlclient-dev \
    && apt-get clean \
    && apt-get -y install curl
RUN mkdir /code
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY . /code/
