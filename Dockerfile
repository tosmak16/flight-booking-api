FROM python:3.7


# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


# add app
COPY . /usr/src/app

# install pipenv
RUN pip install pipenv

# install dependencies
RUN pipenv install --system

EXPOSE 5000

# run server
CMD ["gunicorn", "flight_booking.config.wsgi"]