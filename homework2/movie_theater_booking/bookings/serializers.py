from rest_framework import serializers
from bookings.models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    """
    Create a Movie Serailizer using the Model Serializer class.
    """
    class Meta:
        model = Movie
        fields = [
            'title',
            'description',
            'release_date',
            'duration'
        ]

class SeatSerializer(serializers.ModelSerializer):
    """
    Create a Seat Serailizer using the Model Serializer class.
    """
    class Meta:
        model = Seat
        fields = [
            'seat_row',
            'seat_col',
            'is_booked'
        ]


class BookingSerializer(serializers.ModelSerializer):
    """
    Create a Booking Serailizer using the Model Serializer class.
    """
    class Meta:
        model = Booking
        fields = [
            'movie',
            'seat',
            'user',
            'booking_date'
        ]
