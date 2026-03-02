from behave import given, when, then
from django.contrib.auth.models import User
from django.urls import reverse
from bookings.models import Movie

@given("I am on the home page")
def step_impl(context):
    context.response = context.test.client.get(reverse('home'))
    assert context.response.status_code == 200

@given("\"{movie}\" is an available movie")
def step_impl(context, movie):
    # Create avengers endgame so that it is an available movie.
    try:
        movie = Movie.objects.get(title=movie)
    except Movie.DoesNotExist:
        movie = Movie.objects.create(title=movie,
                                     description="The Avengers is an available movie.",
                                     release_date="2026-04-04",
                                     duration=181
        )
        context.movie = movie

@given("I am logged in as an administrator")
def step_impl(context):
    # Create superuser.
    admin = User.objects.create_superuser(username="admin", password="password.6789")
    context.test.client.login(username=admin.username, password=admin.password)
    context.logged_in_user = admin

@when("I select the movie")
def step_impl(context):
    movie_url = reverse('movie_time', args=(context.movie.id,))
    context.response = context.test.client.get(movie_url)
    assert context.response.status_code == 200

@when("I create a new movie \"{title}\"")
def step_impl(context, title):
    Movie.objects.create(title=title,
                         description="Finding Nemo is the movie.",
                         release_date="2022-04-04",
                         duration=90
    )

@then("I am redirected to the information page")
def step_impl(context):
    assert context.response.status_code == 200

@then("I can see the movie's duration is \"{duration_text}\"")
def step_impl(context, duration_text):
    context.test.assertContains(context.response, duration_text)

@then("the movie \"{movie}\" should exist in the database")
def step_impl(context, movie):
    # Try to retrieve the movie from the database.
    exists = Movie.objects.filter(title=movie).exists()
    context.test.assertTrue(exists)