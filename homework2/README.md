# Homework 1

## Overview of Project
In this project, I was able to interact with Python and write tests for each file I created. This project explores basic Python syntax, datatypes, and control structures as well as more advanced topics such as implementing an algorihtm, using file handing, and implementing tests to check the code.

### Project Structure
```text
bookings/
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── templates
│   ├── bookings
│   │   ├── base.html
│   │   ├── booking_history.html
│   │   ├── movie_list.html
│   │   ├── movie_time.html
│   │   ├── seat_booking.html
│   │   └── signup.html
│   └── registration
│       └── login.html
├── tests.py
├── urls.py
└── views.py
features/
├── authentication.feature
├── booking_history.feature
├── movie_management.feature
├── seat_availability_and_booking.feature
└── steps
    ├── authentication_steps.py
    ├── booking_history_steps.py
    ├── movie_management_steps.py
    └── seat_availability_and_booking_steps.py
media/
└── movie_covers
    ├── Avengers_Endgame.jpg
    ├── Black_Panther.jpg
    ├── Spider_Man_Homecoming.jpg
    ├── Spider_Man_Spider_Verse.jpg
    ├── The_Amazing_Spider_Man.jpg
    └── default.jpg
movie_theater_booking/
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-312.pyc
│   ├── asgi.cpython-312.pyc
│   ├── settings.cpython-312.pyc
│   ├── urls.cpython-312.pyc
│   └── wsgi.cpython-312.pyc
requirements.txt
manage.py
build.sh 
```

## How to Run Locally
#### 1) Open a terminal and create a virtual environment. Then activate the environment.
```
python3 -m venv <name_of_virtual_environment> --system-site-packages
source <name_of_virtual_environment>/bin/activate
```
* Note: The project contains absolute paths in task6.py, task7.py, test_task6.py, and test_task7.py so these instructions are best suited for an environment in DevEdu.

#### 2) Install dependencies.
```
pip install -r requirements.txt
```

#### 3) Clone the repository,
```
cd /home/student
git clone git@github.com:lkarsanb/cs4300.git 
```

* Note: The clone may not work if the SSH connection is not set up properly. If not, the following commands can be used instead.
```
        cd /home/student
        git clone git clone https://github.com/lkarsanb/cs4300.git
```


#### 4) cd into the homework2 directory.
```
cd cs4300/homework2
```

#### 5) From here, you can run migrations.
```
python manage.py makemigrations (this is optional)
python manage.py migrate
```

#### 6) A superuser may also be created at this point.
```
python manage.py createsuperuser
```

#### 7) The project can then be run locally.
```
python manage.py runserver
```
* Note: If using DevEdu, use ``` python manage.py runserver 0.0.0.0:3000 ```

