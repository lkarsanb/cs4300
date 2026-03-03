import datetime
from django.utils import timezone
from behave import given, when, then
from django.contrib.auth.models import User
from django.urls import reverse

from bookings.models import Movie, Seat


@given('I am on the movie "times" page for "{movie_title}"')
def step_impl(context, movie_title):
    # Create movie if needed so that it is an available movie. Also create seat.
    movie, created = Movie.objects.get_or_create(
        title=movie_title,
        description="Black Panther is an available movie.",
        release_date="2026-05-20",
        duration=181,
    )

    context.movie = movie

    show_time = datetime.datetime(2026, 5, 20, 8, 0)
    show_time = timezone.make_aware(show_time)
    Seat.objects.create(
        movie=context.movie,
        movie_location=1,
        movie_time=show_time,
        seat_row="A",
        seat_col=1,
    )

    # On the times page.
    url = reverse("movie_time", args=(movie.id,))
    context.response = context.test.client.get(url)


@given("I am signed in")
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


@given("I am not signed in")
def step_impl(context):
    context.test.client.logout()


@given('I am on the "seats" page for "{title}" on "{date}" at "{time}"')
def step_impl(context, title, date, time):
    datetime_version = datetime.datetime.strptime(f"{date} {time}", "%b %d, %Y %H:%M")
    context.datetime_version = timezone.make_aware(datetime_version)
    # Ensure movie and seat exist for this time.
    context.movie = Movie.objects.create(
        title=title,
        description="Black Panther is an available movie.",
        release_date="2026-05-20",
        duration=181,
    )

    context.test_seat = Seat.objects.create(
        movie=context.movie,
        movie_location=1,
        movie_time=context.datetime_version,
        seat_row="C",
        seat_col=3,
        is_booked=False,
    )

    context.booked_seat, created = Seat.objects.get_or_create(
        movie=context.movie,
        movie_location=1,
        movie_time=context.datetime_version,
        seat_row="A",
        seat_col=1,
        is_booked=True,
    )


@when('I select the available date "{date}"')
def step_impl(context, date):
    date_obj = datetime.datetime.strptime(date, "%b %d, %Y")
    date_obj = timezone.make_aware(date_obj)
    context.selected_date = date_obj.strftime("%Y-%m-%d")
    expected_format = date_obj.strftime("%b %d, %Y")
    context.test.assertContains(context.response, expected_format)


@when('I select "{time}"')
def step_impl(context, time):
    url = reverse("seat_booking", args=(context.movie.id,))
    query = f"?show_date={context.selected_date}&show_time={time}"
    context.response = context.test.client.get(url + query)


@when('I select seat "{seat}" which is available')
def step_impl(context, seat):
    url = reverse(
        "book_selected_seat",
        args=(
            context.movie.id,
            context.test_seat.id,
        ),
    )
    context.response = context.test.client.post(url, follow=True)


@when('I select seat "{seat}" which is already booked')
def step_impl(context, seat):
    url = reverse(
        "book_selected_seat",
        args=(
            context.movie.id,
            context.booked_seat.id,
        ),
    )
    context.response = context.test.client.post(url, follow=True)


@then('I should see "{time}" is an available time')
def step_impl(context, time):
    context.test.assertContains(context.response, time)


@then('I should be redirected to the "log in" page')
def step_impl(context):
    context.test.assertEqual(context.response.status_code, 200)
    final_path = context.response.request["PATH_INFO"]
    context.test.assertIn(reverse("login"), final_path)


@then("after signing in")
def step_impl(context):
    user, created = User.objects.get_or_create(username="user5678")
    user.set_password("password.5678")
    user.save()

    context.test.client.login(username=user.username, password=user.password)
    url = reverse(
        "book_selected_seat",
        args=(
            context.movie.id,
            context.test_seat.id,
        ),
    )
    context.response = context.test.client.post(url, follow=True)


@then("the seat should be booked")
def step_impl(context):
    context.test_seat.refresh_from_db()
    context.test.assertTrue(context.test_seat.is_booked, context.test_seat.seat_row)


@then("I should be redirected to the bookings page")
def step_impl(context):
    final_url = context.response.request.get("PATH_INFO")
    context.test.assertEqual(final_url, reverse("booking_history"))


@then('I should be redirected to the "seats" page')
def step_impl(context):
    expected_url = reverse("seat_booking", args=(context.movie.id,))
    final_url = context.response.request.get("PATH_INFO")
    context.test.assertEqual(final_url, expected_url)


@then("I cannot book the seat")
def step_impl(context):
    context.test_seat.refresh_from_db()
    context.test.assertTrue(context.booked_seat.is_booked)
