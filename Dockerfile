FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y netcat

# add app
COPY . /usr/src/app

# install pipenv
RUN pip install pipenv

# install dependencies
RUN pipenv install --system --skip-lock

EXPOSE 8000

# copy entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# run server
CMD ["gunicorn", "flight_booking.config.wsgi", "--bind 0.0.0.0:8000"]