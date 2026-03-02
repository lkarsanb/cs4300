from django.contrib.admin import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED

from .models import Movie, Seat, Booking
from datetime import date, datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from .admin import SEAT_ROWS, SEAT_COLS, SeatAdmin
User = get_user_model()

# Create your tests here.
class MovieModelTest(TestCase):
    def setUp(self):
        """
        Set up a valid movie that can be used by the tests.
        """
        self.valid_movie = Movie.objects.create(title="Test Movie Title 123 !",
                                                description="Test Movie Description",
                                                release_date=date.today(),
                                                duration=90)

    def test_movie_creation(self):
        """
        Test the movie was properly created.
        """
        self.assertEqual(self.valid_movie.title, "Test Movie Title 123 !")
        self.assertEqual(self.valid_movie.description, "Test Movie Description")
        self.assertEqual(self.valid_movie.release_date, date.today())
        self.assertEqual(self.valid_movie.duration, 90)

    def test_default_image(self):
        """
        Test the default movie cover is used if a movie cover is not uploaded.
        """
        self.assertEqual(self.valid_movie.image, "movie_covers/default.jpg")

    def test_str_method(self):
        """
        Test the str method is correctly formatted.
        """
        self.assertEqual(str(self.valid_movie), "Test Movie Title 123 !")

    def test_title_length(self):
        """
        Test that the length of the title must be less than 255 characters.
        """
        title = "Test Movie Title" * 200
        movie = Movie.objects.create(title=title,
                             description="Test Movie Description",
                             release_date=date.today(),
                             duration=90)
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_title_length_exact(self):
        """
        Test that the title can be exactly 255 characters.
        """
        title = "A" * 255
        movie = Movie.objects.create(title=title,
                                     description="Test Movie Description",
                                     release_date=date.today(),
                                     duration=90)

        self.assertEqual(movie.title, title)
        self.assertEqual(movie.description, "Test Movie Description")
        self.assertEqual(movie.release_date, date.today())
        self.assertEqual(movie.duration, 90)


    def test_duration_positive(self):
        """
        Test that the duration is positive.
        """
        duration = -100
        with self.assertRaises(IntegrityError):
            Movie.objects.create(title="title",
                                 description="Test Movie Description",
                                 release_date=date.today(),
                                 duration=duration)


class SeatModelTest(TestCase):
    def setUp(self):
        """"
        Create valid seat to be used by tests.
        """
        self.movie = Movie.objects.create(title="Seat Test Movie Title",
                                          description="Another Test Movie Description",
                                          release_date=date.today(),
                                          duration=180)
        self.seat = Seat.objects.create(movie=self.movie,
                                        movie_location=1,
                                        movie_time=timezone.now(),
                                        seat_row="A",
                                        seat_col=1)

    def test_default_is_booked(self):
        """
        Test the default of seat is not booked (is_booked = False).
        """
        self.assertFalse(self.seat.is_booked)

    def test_str_method_when_is_booked(self):
        """
        Test the str method is correctly formatted when a seat is booked.
        """
        self.seat.is_booked = True
        self.seat.save()
        self.assertEqual(str(self.seat), "Seat Test Movie Title: Theater 1 Seat A1 (Unavailable)")

    def test_str_method_when_is_not_booked(self):
        """
        Test the str method is correctly formatted when a seat is not booked.
        """
        self.seat.is_booked = False
        self.seat.save()
        self.assertEqual(str(self.seat), "Seat Test Movie Title: Theater 1 Seat A1 (Available)")

    def test_future_booking_time(self):
        """
        Test the clean method that the movie cannot be boo
        ked if it has not been released yet.
        """
        release_date = date(3000, 1, 1)
        future_movie = Movie.objects.create(title="Future Movie Title",
                                            description="Test Movie Description",
                                            release_date=release_date,
                                            duration=180)

        seat = Seat.objects.create(movie=future_movie,
                                   movie_location=1,
                                   movie_time=timezone.now(),
                                   seat_row="A",
                                   seat_col=1)
        with self.assertRaises(ValidationError):
            seat.clean()

    def test_invalid_seat_row_as_more_than_one_char(self):
        """
        Test that invalid seat row raises an error.
        """
        seat = Seat.objects.create(movie=self.movie,
                                   movie_location=1,
                                   movie_time=timezone.now(),
                                   seat_row="Hello",
                                   seat_col=1)
        with self.assertRaises(ValidationError):
            seat.full_clean()


    def test_invalid_seat_row(self):
        """
        Test that the clean method ensures seat row is A-F.
        """
        seat_row = "J"
        seat = Seat.objects.create(movie=self.movie,
                                   movie_location=1,
                                   movie_time=timezone.now(),
                                   seat_row=seat_row,
                                   seat_col=1)
        with self.assertRaises(ValidationError):
            seat.clean()

    def test_invalid_seat_col(self):
        """
        Test that the clean method ensures seat col is 1-6.
        """
        seat_col = 100
        seat = Seat.objects.create(movie=self.movie,
                                   movie_location=1,
                                   movie_time=timezone.now(),
                                   seat_row="A",
                                   seat_col=seat_col)
        with self.assertRaises(ValidationError):
            seat.clean()

    def test_seat_unique_constraint(self):
        """Test that the same seat, time, and location cannot be booked."""
        movie_time = timezone.make_aware(datetime(2000, 1, 1, 13, 1, 0))
        Seat.objects.create(movie=self.movie,
                            movie_location=1,
                            movie_time=movie_time,
                            seat_row="A",
                            seat_col=1)

        with self.assertRaises(IntegrityError):
            Seat.objects.create(movie=self.movie,
                                movie_location=1,
                                movie_time=movie_time,
                                seat_row="A",
                                seat_col=1)

class BookingModelTest(TestCase):
    def setUp(self):
        """
        Create a valid booking to be used by tests.
        """
        self.test_movie = Movie.objects.create(title="Another Test Movie Title",
                                          description="Another Test Movie Description",
                                          release_date=date.today(),
                                          duration=180)
        self.test_seat = Seat.objects.create(movie=self.test_movie,
                                        movie_location=2,
                                        movie_time=timezone.now(),
                                        seat_row="A",
                                        seat_col=2)
        self.test_user = User.objects.create(username="Test User")
        self.booking = Booking.objects.create(movie=self.test_movie,
                                              seat=self.test_seat,
                                              user=self.test_user,
                                              booking_date=timezone.now())

    def test_str_method(self):
        """
        Test that the string method is correctly formatted.
        """
        self.assertEqual(str(self.booking), "Test User: Another Test Movie Title (A2)")

    def test_create_booking(self):
        """
        Test that a valid booking is created.
        """
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(self.booking.movie.title, "Another Test Movie Title")
        self.assertEqual(self.booking.seat, self.test_seat)
        self.assertEqual(self.booking.user, self.test_user)
        self.assertIn("Test Movie", str(self.booking))

class ViewTest(TestCase):
    def setUp(self):
        """
        Create valid user, movie, and seat to be used by tests.
        """
        self.time = timezone.now()
        self.movie = Movie.objects.create(title="Another Test Movie Title",
                                          description="Another Test Movie Description",
                                          release_date=date.today(),
                                          duration=180)
        self.seat = Seat.objects.create(movie=self.movie,
                                        movie_location=2,
                                        movie_time=self.time,
                                        seat_row="A",
                                        seat_col=2)
        self.user = User.objects.create(username="Test User", password="TestPass")
        self.booking = Booking.objects.create(movie=self.movie,
                                              seat=self.seat,
                                              user=self.user,
                                              booking_date=timezone.now())

    def test_movie_list_html(self):
        """
        Test that the movie_list_html function returns a list of movies.
        :return:
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/movie_list.html")
        self.assertContains(response, "Another Test Movie Title")

    def test_movie_time_html_valid_movie(self):
        """
        Test that the movie_time_html returns valid information if a valid movie_id is given.
        """
        response = self.client.get(reverse("movie_time", args=(self.movie.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/movie_time.html")
        self.assertContains(response, "Another Test Movie Title")

    def test_movie_time_html_invalid_movie(self):
        """
        Test that the movie_time_html returns valid information if an invalid movie_id is given.
        """
        invalid_id = 100
        url = reverse("movie_time", args=(invalid_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_movie_time_html_only_unique_dates(self):
        """
        Ensure that only one movie time is being returned, not one per each seat.
        """
        time = timezone.now()

        # Create multiple seats for 1 movie.
        for i in range(3):
            Seat.objects.create(movie=self.movie,
                                movie_location=i,
                                movie_time=time,
                                seat_row="A",
                                seat_col=i + 1)

        url = reverse("movie_time", args=(self.movie.id,))
        response = self.client.get(url)
        dates = response.context["dates"]

        # Check there is only 1 date.
        self.assertEqual(len(dates), 1)
        self.assertIn(time.date(), dates)

    def test_movie_time_html_no_showings(self):
        no_showing_movie = Movie.objects.create(title="No showings",
                                                description="No showings",
                                                release_date=date.today(),
                                                duration=100)
        url = reverse("movie_time", args=(no_showing_movie.id,))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "bookings/movie_time.html")
        self.assertEqual(response.context["dates"], {})

    def test_seat_booking_html_valid(self):
        """
        Test that valid seat booking is created and query parameters are correct..
        :return:
        """
        my_date = "2026-05-20"
        my_time = "14:00:00"
        datetime_version = datetime(2026, 5, 20, 14, 0, 0)
        datetime_version = timezone.make_aware(datetime_version)
        my_seat = Seat.objects.create(movie=self.movie,
                                      movie_location=1,
                                      movie_time=datetime_version,
                                      seat_row="A",
                                      seat_col=1)
        url = reverse("seat_booking", args=(self.movie.id,))
        query_string = f"?show_date={my_date}&show_time={my_time}"

        response = self.client.get(url + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertIn(my_seat, response.context["seats"])

    def test_seat_booking_html_invalid_id(self):
        """
        Test that 404 is returned if an invalid movie id is given.
        """
        invalid_movie_id = 100
        url = reverse("seat_booking", args=(invalid_movie_id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_seat_booking_html_sold_out(self):
        """
        Test that sold_out = True when all seats are booked.
        """
        datetime_version = datetime(2026, 5, 20, 14, 0, 0)
        datetime_version = timezone.make_aware(datetime_version)

        booked_seat = Seat.objects.create(movie=self.movie,
                                          movie_location=1,
                                          movie_time=datetime_version,
                                          seat_row="A",
                                          seat_col=1,
                                          is_booked=True)
        my_date = booked_seat.movie_time.strftime("%Y-%m-%d")
        my_time = booked_seat.movie_time.strftime("%H:%M:%S")

        url = reverse("seat_booking", args=(self.movie.id,))
        query_string = f"?show_date={my_date}&show_time={my_time}"

        response = self.client.get(url + query_string)
        self.assertTrue(response.context["is_sold_out"])

    def test_seat_booking_html_invalid_format(self):
        """
        Test if invalid values are passed into query_string.
        """
        url = reverse("seat_booking", args=(self.movie.id,))
        query_string = "?show_date=NOT_A_DATE&show_time=NOT_A_TIME"
        response = self.client.get(url + query_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["seats"]), 0)

    def test_booking_history_html_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("booking_history"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["bookings"]), 1)

    def test_booking_history_html_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("booking_history"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["bookings"]), 0)

    def test_process_booking_valid(self):
        """
        Tests if authenticated user can make a booking.
        """
        self.client.force_login(self.user)
        self.assertFalse(self.seat.is_booked)

        url = reverse("book_selected_seat", args=(self.movie.id, self.seat.id))
        response = self.client.post(url)
        self.assertRedirects(response, reverse("booking_history"))

        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_process_booking_unauthenticated(self):
        """
        Tests if unauthenticated user can make a booking.
        """
        self.client.logout()
        url = reverse("book_selected_seat", args=(self.movie.id, self.seat.id))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_already_booked(self):
        """
        Test if user tries to book seat that is already booked.
        """
        self.client.force_login(self.user)
        self.seat.is_booked = True
        self.seat.save()
        initial_num_bookings = Seat.objects.count()
        url = reverse("book_selected_seat", args=(self.movie.id, self.seat.id))
        response = self.client.post(url)

        self.assertRedirects(response, reverse("booking_history"))
        self.assertEqual(Booking.objects.count(), initial_num_bookings)

    def test_process_booking_get_method(self):
        """
        GET request should be redirected to home page without booking.
        """
        self.client.force_login(self.user)
        url = reverse("book_selected_seat", args=(self.movie.id, self.seat.id))
        response = self.client.get(url)

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Seat.objects.get(id=self.seat.id).is_booked)

    def test_cancel_booking_html_valid(self):
        """
        Test that a booking can be canceled and the seat is available.
        """
        self.client.force_login(self.user)

        self.seat.is_booked = True
        self.seat.save()
        booking = Booking.objects.create(user=self.user,
                                         movie=self.movie,
                                         seat=self.seat)
        initial_num_bookings = Booking.objects.count()
        url = reverse("cancel_booking", args=(booking.id,))

        response = self.client.post(url)
        self.assertRedirects(response, reverse("booking_history"))
        self.assertEqual(Booking.objects.count(), initial_num_bookings - 1)

        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)

    def test_cancel_booking_invalid_id(self):
        """
        Tests that there is a 404 error if booking id is invalid.
        """
        self.client.force_login(self.user)
        invalid_id = 9999
        url = reverse("cancel_booking", args=(invalid_id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_cancel_booking_diff_user(self):
        """
        Test that another user cannot cancel other users' bookings.
        :return:
        """
        user = User.objects.create(username="good", password="1234")
        booking = Booking.objects.create(user=user,
                                         movie=self.movie,
                                         seat=self.seat)

        # self.user trying to access user's booking.
        self.client.force_login(self.user)
        url = reverse("cancel_booking", args=(booking.id,))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_signup_html_valid(self):
        """
        Test that the signup page loads.
        """
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/signup.html")
        self.assertIn("form", response.context)

    def test_signup_html_successful(self):
        """
        Test that a user can create an account.
        """
        initial_user_count = User.objects.count()
        data = {
            "username": "user123",
            "password1": "Test.1234!!",
            "password2": "Test.1234!!"
        }

        response = self.client.post(reverse("signup"), data=data)

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(User.objects.count(), initial_user_count + 1)
        self.assertTrue(User.objects.filter(username="user123").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_signup_unsuccessful(self):
        """
        Test that user cannot sign in if username is same as another user or alrady have an account.
        :return:
        """
        User.objects.create(username="user123", password="Test,1234!!")
        initial_user_count = User.objects.count()
        data = {
            "username": "user123",
            "password1": "Test.1234!!",
            "password2": "Test.1234!!"
        }

        response = self.client.post(reverse("signup"), data=data)
        self.assertEqual(User.objects.count(), initial_user_count)
        self.assertEqual(response.status_code,200)
        self.assertFalse(response.context["form"].is_valid())

class TestAdmin(TestCase):
    def setUp(self):
        datetime_version = datetime(2026, 5, 20, 14, 0, 0)
        self.datetime_version = timezone.make_aware(datetime_version)
        self.site = AdminSite()
        self.movie = Movie.objects.create(title="Movie Title",
                                          description="Test Movie Description",
                                          release_date=self.datetime_version.date(),
                                          duration=100)
        self.seat = Seat.objects.create(movie=self.movie,
                                        movie_location=1,
                                        movie_time=self.datetime_version,
                                        seat_row="A",
                                        seat_col=1)


    def test_generate_seats(self):
        """
        Test admin action that creates seats. Ensure it creates correct number of seats.
        """
        admin = User.objects.create_superuser(username="admin", password="super.1234")
        self.client.force_login(admin)
        url = reverse("admin:bookings_seat_changelist")

        data = {
            "action": "generate_seats",
            "_selected_action": [self.seat.id],
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        expected_total = len(SEAT_ROWS) * len(SEAT_COLS)
        self.assertEqual(Seat.objects.count(), expected_total)

class BookingHistoryHtmlTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="TestUser", password="TestPass")
        self.movie1 = Movie.objects.create(title="Test1 Movie Title",
                                           description="Test1 Movie Description",
                                           release_date=date.today(),
                                           duration=90)
        self.movie2 = Movie.objects.create(title="Test2 Movie Title",
                                           description="Test2 Movie Description",
                                           release_date=date.today(),
                                           duration=100)
        self.movie3 = Movie.objects.create(title="Test3 Movie Title",
                                           description="Test3 Movie Description",
                                           release_date=date.today(),
                                           duration=110)
        self.seat = Seat.objects.create(movie=self.movie1,
                                        seat_row="A",
                                        seat_col=1,
                                        movie_time=timezone.now(),
                                        movie_location=1)
        self.booking = Booking.objects.create(movie=self.movie2,
                                              user=self.user,
                                              seat=self.seat,
                                              booking_date=date.today().strftime("%Y-%m-%d"))
        self.url = reverse("booking_history")


    def test_movie_list_html(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/movie_list.html")
        movies = response.context["movies"]
        self.assertEqual(len(movies), 3)
        self.assertIn(self.movie1, movies)
        self.assertIn(self.movie2, movies)
        self.assertIn(self.movie3, movies)

    def test_get_movie(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_booking_history_html(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bookings", response.context)
        self.assertEqual(len(response.context["bookings"]), 1)
        self.assertEqual(response.context["bookings"][0], self.booking)

    def test_not_authenticated_user_booking_history_html(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["bookings"], [])


class MovieAPITest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title="Another Test Movie Title",
                                          description="Another Test Movie Description",
                                          release_date=date.today(),
                                          duration=100)
        self.url = reverse("movie-list")
        self.client = APIClient()

    def test_get_movie_list(self):
        """
        Tests getting a list.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("Another Test Movie Title", response.content.decode())
        self.assertEqual(len(response.data), 1)

    def test_get_movie_details(self):
        url = reverse("movie-detail", args=(self.movie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json().get("title"), self.movie.title)
        self.assertEqual(response.json().get("description"), self.movie.description)
        self.assertEqual(response.json().get("release_date"), self.movie.release_date.strftime("%Y-%m-%d"))
        self.assertEqual(response.json().get("duration"), self.movie.duration)

    def test_create_movie(self):
        data = {
            "title": "Test Movie Title",
            "description": "Test Movie Description",
            "release_date": date.today(),
            "duration": 90,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_invalid_movie_id(self):
        url = reverse("movie-detail", args=[1000000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_create_movie_missing_title(self):
        data = {
            "description": "Test Movie Description",
            "release_date": date.today(),
            "duration": 90,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_update_movie(self):
        """
        Test updating (PUT) of a movie.
        """
        url = reverse("movie-detail", args=(self.movie.id,))
        data = {
            "title": "New Test Movie Title",
            "description": "New Test Movie Description",
            "release_date": date.today(),
            "duration": 100,
        }

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json().get("title"), data["title"])
        self.assertEqual(response.json().get("description"), data["description"])
        self.assertEqual(response.json().get("release_date"), data["release_date"].strftime("%Y-%m-%d"))
        self.assertEqual(response.json().get("duration"), data["duration"])

    def test_delete_movie(self):
        url = reverse("movie-detail", args=(self.movie.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)


class SeatAPITest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title="Another Test Movie Title",
                                          description="Another Test Movie Description",
                                          release_date=date.today(),
                                          duration=100)
        self.seat = Seat.objects.create(movie=self.movie,
                                        movie_location=2,
                                        movie_time=timezone.now(),
                                        seat_row="A",
                                        seat_col=2)

    def test_get_seat(self):
        url = reverse("seat-detail", args=(self.seat.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)



class BookingAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Test User", password="TestPass")
        self.non_user = User.objects.create(username="Non User")
        self.movie = Movie.objects.create(title="Another Test Movie Title",
                                          description="Another Test Movie Description",
                                          release_date=date.today(),
                                          duration=100)
        self.seat = Seat.objects.create(movie=self.movie,
                                        movie_location=2,
                                        movie_time=timezone.now(),
                                        seat_row="A",
                                        seat_col=2)
        self.booking = Booking.objects.create(movie=self.movie,
                                              seat=self.seat,
                                              user=self.user,
                                              booking_date=date.today())
        self.url = reverse("booking-detail", args=(self.booking.id,))
        self.client = APIClient()

    def test_booking_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_already_booked_seat(self):
        url = reverse("booking-detail", args=(self.seat.id,))
        self.client.force_login(self.user)
        self.seat.is_booked = True
        self.seat.save()
        data = {
            "movie": self.movie.id,
            "user": self.user.id,
            "seat": self.seat.id,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
