from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet

# Instantiate register.
router = DefaultRouter()

# Register the viewsets with the router.
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = router.urls
urlpatterns += [
    path('api-path', include("rest_framework.urls")),
]