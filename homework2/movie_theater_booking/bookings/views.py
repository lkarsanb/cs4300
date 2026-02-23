from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    '''
    Create ViewSet for Movies here that uses normal CRUD operations inherited from ModelViewSet.
    '''
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class SeatViewSet(viewsets.ModelViewSet):
    '''
    Create ViewSet for Seats here that uses normal CRUD operations inherited from ModelViewSet
    in addition to custom action for booking.
    '''
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

    # @action(detail=True, methods=['post'])
    # def book_seat(self, request):
    #     '''
    #     A custom action that can be used to send a response with information about the seat selected.
    #     '''
    #     seat = self.get_object()
    #     if seat.is_booked:
    #         # Seat is already booked.
    #         return Response({'Status': 'Already Booked'})
    #     else:
    #         # Seat is not booked, so can book it.
    #         seat.is_booked = True
    #         seat.save()
    #         return Response({'Status': 'Booked Seat'})


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]