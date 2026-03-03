import datetime

from behave import given, when, then
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from bookings.models import Movie, Seat, Booking


@given("I am signed in to my account")
def step_impl(context):
    # Create a user in database
    try:
        user = User.objects.get(username="user5678", password="password.5678")
    except User.DoesNotExist:
        user = User.objects.create_user(username="user5678", password="password.5678")
    context.user = user

    login_successful = context.test.client.login(
        username="user5678", password="password.5678"
    )
    context.test.assertTrue(login_successful)


@given('I have a booking for "{movie_title}"')
def step_impl(context, movie_title):
    movie_time = datetime.datetime(2026, 5, 20, 13, 0)
    movie_time = timezone.make_aware(movie_time)
    movie, created = Movie.objects.get_or_create(
        title=movie_title,
        description="This is a movie",
        release_date="2026-05-20",
        duration=100,
    )
    seat = Seat.objects.create(
        movie=movie, movie_time=movie_time, movie_location=1, seat_row="A", seat_col=1
    )
    context.booking = Booking.objects.create(user=context.user, movie=movie, seat=seat)


@given("I am on the bookings page")
def step_impl(context):
    context.response = context.test.client.get(reverse("booking_history"))
    assert context.response.status_code == 200


@when("I view my booking history")
def step_impl(context):
    url = reverse("booking_history")
    context.response = context.test.client.get(url)


@then("I can delete the booking")
def step_impl(context):
    url = reverse("cancel_booking", args=(context.booking.id,))
    context.response = context.test.client.get(url, follow=True)


@then('I should see "{movie}" in the list')
def step_impl(context, movie):
    context.test.assertContains(context.response, movie)


@then('"{movie}" will no longer be shown on my booking history')
def step_impl(context, movie):
    context.test.assertNotContains(context.response, movie)

    exists = Booking.objects.filter(id=context.booking.id).exists()
    context.test.assertFalse(exists)
    context.booking.seat.refresh_from_db()
    context.test.assertFalse(context.booking.seat.is_booked)
