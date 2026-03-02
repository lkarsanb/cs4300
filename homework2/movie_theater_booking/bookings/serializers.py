from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    """
    Create a Movie Serializer using the Model Serializer class.
    """
    class Meta:
        model = Movie
        fields = "__all__"

class SeatSerializer(serializers.ModelSerializer):
    """
    Create a Seat Serializer using the Model Serializer class.
    """
    class Meta:
        model = Seat
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    """
    Create a Booking Serializer using the Model Serializer class.
    """
    class Meta:
        model = Booking
        fields = "__all__"
