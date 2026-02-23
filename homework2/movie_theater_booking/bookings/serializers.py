from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.Serializer):
    class Meta:
        model = Movie
        fields = (
            'title',
            'description',
            'release_date',
            'duration'
        )

class SeatSerializer(serializers.Serializer):
    class Meta:
        model = Seat
        fields = (
            'seat_row',
            'seat_col',
            'is_booked'
        )


class BookingSerializer(serializers.Serializer):
    class Meta:
        model = Booking
        fields = (
            'movie',
            'seat',
            'users',
            'booking_date'
        )
