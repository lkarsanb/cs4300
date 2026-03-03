from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

# Get user to be used for booking model.
User = get_user_model()

# Define variables to later clean data for valid rows and columns.
SEAT_ROWS = ["A", "B", "C", "D", "E", "F"]
SEAT_COLS = [1, 2, 3, 4, 5, 6]


# Create your models here.
class Movie(models.Model):
    """
    Class for a movie model. Creates initial attributes including title, description, release date, duration, and image.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=750)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    image = models.ImageField(
        upload_to="movie_covers/", default="movie_covers/default.jpg"
    )

    def __str__(self):
        """Returns the title of the movie."""
        return self.title


class Seat(models.Model):
    """
    Class for a seat model. Creates initial attributes including movie, movie location, seat number and booking status.
    """

    # Seats are arranged in such a way that first letter is row and following 2 digits are the column.
    # Ex) F12 is 12th seat in row F.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_location = models.PositiveSmallIntegerField(
        help_text="Theater 1-5"
    )  # Movie theater from 1 to 5.
    movie_time = models.DateTimeField()
    seat_row = models.CharField(max_length=1, help_text="Seat Row (A-F)")
    seat_col = models.PositiveIntegerField(help_text="Seat Column (1-6)")

    # Booking status where True = seat is taken and False = seat is free.
    is_booked = models.BooleanField(default=False)

    class Meta:
        """
        Use the Meta class to create restrains on instances of seats.
        """

        # Each seat must have unique row, column, location, and movie.
        constraints = [
            UniqueConstraint(
                fields=[
                    "movie",
                    "movie_location",
                    "movie_time",
                    "seat_row",
                    "seat_col",
                ],
                name="unique_seats",
            )
        ]

    def clean(self):
        # Ensure that no movies are playing before their release date.
        if self.movie_time.date() < self.movie.release_date:
            raise ValidationError(
                f"{self.movie} is not released until {self.movie.release_date}"
            )

        # Ensure valid rows and columns are entered.
        if self.seat_row.upper() not in SEAT_ROWS:
            raise ValidationError(
                f"{self.seat_row} is not a valid seat row. Please select row between {SEAT_ROWS[0]} and {SEAT_ROWS[-1]}"
            )
        if self.seat_col not in SEAT_COLS:
            raise ValidationError(
                f"{self.seat_col} is not a valid seat column. Please select column between {SEAT_COLS[0]} and {SEAT_COLS[-1]}"
            )

    def __str__(self):
        """Create human readable version of information."""
        if self.is_booked:
            status = "Unavailable"
        else:
            status = "Available"
        return f"{self.movie.title}: Theater {self.movie_location} Seat {self.seat_row}{self.seat_col} ({status})"


class Booking(models.Model):
    """
    Class for a booking model. Creates initial attributes including movie, seat, user, and booking date.
    """

    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE
    )  # The movie is the Movie model.
    seat = models.ForeignKey(
        Seat, on_delete=models.CASCADE
    )  # The seat is the Seat model.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Create human readable version of information."""
        return f"{self.user}: {self.movie.title} ({self.seat.seat_row}{self.seat.seat_col})"
