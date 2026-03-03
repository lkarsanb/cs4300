from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


# Class based views for API.
class MovieViewSet(viewsets.ModelViewSet):
    """
    Create ViewSet for Movies here that uses normal CRUD operations inherited from ModelViewSet.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class SeatViewSet(viewsets.ModelViewSet):
    """
    Create ViewSet for Seats here that inherits from ModelViewSet.
    """

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    """
    Create ViewSet for Bookings here that inherits from ModelViewSet.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


# Function based views for the HTML templates.
def movie_list_html(request):
    """
    Returns all of the movies currently in database.
    :param request: HTTP request containing information about the request.
    :return: HTTP response containing all the movies currently in database.
    """
    movies = Movie.objects.all()
    return render(request, "bookings/movie_list.html", {"movies": movies})


def movie_time_html(request, movie_id):
    """
    Returns the times and dates for a certain movie.
    :param request: HTTP request containing information about the request.
    :param movie_id: The id of movie dates and times are needed for.
    :return: HTTP response containing movies and dates with times.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    showings = Seat.objects.filter(movie=movie)
    dates = {}
    # For each showing associated with a seat, get the time and date and add to a set (to ensure unique).
    for show in showings:
        show_date = show.movie_time.date()
        show_time = show.movie_time.time()
        if show_date not in dates:
            dates[show_date] = set()
        dates[show_date].add(show_time)

    # Sort the times from earlier to later.
    for date in dates:
        dates[date] = sorted(dates[date])
    sort_dates = dict(sorted(dates.items()))

    return render(request, "bookings/movie_time.html", {"movie": movie, "dates": dates})


def seat_booking_html(request, movie_id):
    """
    Returns the seating information about a certain movie at a time.
    :param request: HTTP request containing information about the request.
    :param movie_id: The title of movie the seats are needed for.
    :return:
    """
    movie = get_object_or_404(Movie, id=movie_id)
    # Get the information about the movie time and date the user selected.
    show_time = request.GET.get("show_time")
    show_date = request.GET.get("show_date")

    # If the time and date are not null, convert to datetime and filter seats based on the movie, time, and date.
    if show_time and show_date:
        try:
            showing_time = datetime.strptime(show_time, "%H:%M:%S").time()
            showing_date = datetime.strptime(show_date, "%Y-%m-%d").date()
            seats = Seat.objects.filter(
                movie=movie,
                movie_time__time=showing_time,
                movie_time__date=showing_date,
            ).order_by("seat_row", "seat_col")
        except ValueError:
            seats = Seat.objects.none()
    else:
        seats = Seat.objects.none()

    # A boolean to keep track of which movies are sold out.
    is_sold_out = not seats.filter(is_booked=False).exists()
    return render(
        request,
        "bookings/seat_booking.html",
        {"movie": movie, "seats": seats, "is_sold_out": is_sold_out},
    )


def booking_history_html(request):
    """
    Returns the booking history information for a user.
    :param request: HTTP request containing information about the request.
    :return: The booking history for the user.
    """
    # The user must be signed in to see bookings.
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
    else:
        bookings = []
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


@login_required
def process_booking(request, movie_id, seat_id):
    """
    Handles the user selecting a seat to book.
    :param request: HTTP request containing information about the request.
    :param movie_id: The id of the movie that is booked.
    :param seat_id: The seat the user booked.
    :return:
    """
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=movie_id)
        seat = get_object_or_404(Seat, id=seat_id, movie=movie)

        # If the seat is available, change its status, save status, and create the booking.
        if not seat.is_booked:
            seat.is_booked = True
            seat.save()
            Booking.objects.create(user=request.user, seat=seat, movie=movie)

        # Send user to bookings page to view the booking.
        return redirect("booking_history")
    messages.error(
        request,
        "Must be logged in to book a seat. Please try booking again after signing in.",
    )
    return redirect("home")


def cancel_booking_html(request, booking_id):
    """
    Handles uses deleting a booking.
    :param request: HTTP request containing information about the request.
    :param booking_id: The id of the booking.
    :return: Deletes the booking and reloads bookings page.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Make seat available again.
    booking.seat.is_booked = False
    # Save the seat.
    booking.seat.save()

    booking.delete()
    return redirect("booking_history")


def signup_html(request):
    """
    Handles creating accounts for new users to create bookings.
    :param request: HTTP request containing information about the request.
    :return: An HTTP response with the signup form or redirects user to home page if they successfully created an account.
    """
    # If form has been submitted, create the user if form is valid. Using the django UserCreationForm to handle creating accounts.
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    # Display form.
    else:
        form = UserCreationForm()
    return render(request, "bookings/signup.html", {"form": form})
