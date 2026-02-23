from django.db import models
from django.contrib.auth import get_user_model

# Get user to be used for booking model.
User = get_user_model()

# Create your models here.
class Movie(models.Model):
    """
    Class for a movie model. Creates initial attributes including title, description, release date, and duration.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=750)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    image = models.ImageField(upload_to='movie_covers/')

    def __str__(self):
        """Create human readable version of information."""
        return self.title


class Seat(models.Model):
    """
    Class for a seat model. Creates initial attributes including seat number and booking status.
    """
    # Seats are arranged in such a way that first letter is row and following 2 digits are the column.
    # Ex) F12 is 12th seat in row F.
    seat_row = models.CharField(max_length=1)
    seat_col = models.PositiveIntegerField()

    # Booking status where True = seat is taken and False = seat is free.
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        """Create human readable version of information."""
        if self.is_booked:
            status = "Unavailable"
        else:
            status = "Available"
        return f"Status of {self.seat_row}{self.seat_col}: {status}"



class Booking(models.Model):
    """
    Class for a booking model. Creates initial attributes including movie, seat, user, and booking date.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)    # The movie is the Movie model.
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)      # The seat is the Seat model.
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Create human readable version of information."""
        return f"{self.user}: {self.movie.title} ({self.seat.seat_row}{self.seat.seat_col})"