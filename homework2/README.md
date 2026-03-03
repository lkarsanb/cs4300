# Homework 2

### Overview of Project
In this project, I was able to interact with Python, Django, Django REST Framework, Bootstrap, and render to create a movie booking website. Users are able to view movies that are playing, book seats, and view previous bookings.

## API EndPoints
- /api/movies/
- /api/seats/
- /api/bookings/

## Website Design
- Movies page which is the home page of the website that allows users to view all movies showing.
- Movie times page which shows the dates and times the selected movie is available.
- Seats page where uses can see available seets and book a seat.
- Bookings history page where users that are logged in are able to their bookings (past and future).

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


#### 2) Clone the repository,
```
git clone git@github.com:lkarsanb/cs4300.git 
```

* Note: The clone may not work if the SSH connection is not set up properly. If not, the following commands can be used instead.
  
    ```
     git clone https://github.com/lkarsanb/cs4300.git
    ```


#### 3) cd into the movie_theater_booking directory (where manage.py is located).
```
cd cs4300/homework2/movie_theater_booking
```

#### 4) Install dependencies.
```
pip install -r requirements.txt
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
* Note if running on DevEdu, use
  ```
  python manage.py runserver 0.0.0.0:3000
  ```


## Deployment on Render
Render is used to deploy this project as ``` https://cs4300-movie-booking-9hci.onrender.com/ ```.

## Testing 
This project was tested with unit tests, integration tests, and behavior driven tests.

### For unit and integration testing:
#### 1) Ensure you are in the directory where manage.py is located. If DEBUG = False in settings.py, since there are static files in this project, the following commands must be run.
```
python manage.py collectstatic --noinput
python manage.py test
```

#### If DEBUG = True, then only the following command must be run:
```
python manage.py test
```


#### 2) To get a coverage report of the tests, run:
``` 
coverage run --source='.' manage.py test bookings
```

#### To see the coverage report, run:
```
coverage report
```

### For behavior driven tests:
#### Ensure you are in the directory where manage.py is located. If DEBUG = False in settings.py, since there are static files in this project, the following commands must be run.
```
python manage.py collectstatic --noinput
python manage.py behave <optional path to certain .feature file>
```

#### If DEBUG = True, then only the following command must be run:
lowing commands must be run.
```
python manage.py behave <optional path to certain .feature file>
```


## AI Usage
Artificial Intelligence (AI) was used in this project in various aspects. ChatGPT was used to help plan how to work on the project as well as with understanding how the backend of the application should work. From there, I was able to refer to the documentation to better see how to implement the concepts. ChatGPT was also used for testing and to help identify any missing edge cases as well as to help debug.

In addition to this, the logo that is used on the webpage was created by Gemini.

The pictures that are used in the website are provided by The Movie Database (https://www.themoviedb.org/?language=en-US).

## Note of DEBUG = True in Production Environment
I wanted to try to add images to the website for a better UX. However, I was unaware that Render does not store images for free and requires a paid plan until deployment. I considered the tradeoffs such as changing the images to static but did not think that this was a good design choice due the loss of flexibility and because the information is meant to be uploaded by an admin, so this should not be considered static data which is why I did not make it static from the start. I also considered removing the images, but did not think that this would allow for a good UX and thought that it would be a fun element to implement and learn more about. I also looked into using URLs but saw that this would require persistant storage which would also be a problem with deployment on Render. While it is not a perfect solution, I decided to leave DEBUG as True to keep the images and overall flexibility of the program without changing the underlying structure of the project.
