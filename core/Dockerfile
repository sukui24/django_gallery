# pull official base image
FROM python:3.11

# set work directory
WORKDIR /usr/src/app/core

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get install -y ncat
RUN apt-get update -y \
    && apt-get install postgresql gcc python3-dev musl-dev -y

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . .
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypiont
COPY ./entrypoint.sh .
# copy project
COPY . .


ENTRYPOINT ["./entrypoint.sh"]
