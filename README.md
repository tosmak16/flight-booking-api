[![Coverage Status](https://coveralls.io/repos/github/tosmak16/flight-booking-api/badge.svg?branch=develop)](https://coveralls.io/github/tosmak16/flight-booking-api?branch=develop) [![CircleCI](https://circleci.com/gh/tosmak16/flight-booking-api.svg?style=svg)](https://circleci.com/gh/tosmak16/flight-booking-api) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
# flight-booking-api
A flight booking API that enables a user to log in, upload passport photographs, book tickets, receive tickets as an email, check the status of their flight and make flight reservations purchase tickets.


### Prerequisites

- Clone the repo.
- Change into the directory `$ cd /flight-booking-api`
- Create a `.env` file in your root directory as described in `.env.sample` file.
- Install Python 3.7.x
- To setup pyenv run the following commands: 
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
```
Run $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
```
```
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
```
```
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

#### To install pipenv
```
Run pip install pipenv
```

### Installing

#### To install dependences run the command below
```
pipenv install
```

### Runnning the app

To run the application:

- Run migrations

```
python manage.py migrate
```

- Start the server

```
Python manage.py runserver
```

## Running the tests

`pipenv run test`

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Postgres](https://www.postgresql.org/) - Object-relational database used.
* [Django rest framework](https://django-rest-framework.org) - A powerful and flexible toolkit for building Web APIs.



## Contributing

- Fork this repository to your GitHub account
- Clone the forked repository
- Create your feature branch
- Commit your changes
- Push to the remote branch
- Open a Pull Request

## Authors

* **Oluwatosin Akinola**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details


