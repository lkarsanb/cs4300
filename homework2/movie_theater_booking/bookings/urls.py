from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet
from . import views

# Instantiate register.
router = DefaultRouter()

# Register the viewsets with the router.
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")


urlpatterns = [
    # HTML Templates
    path("", views.movie_list_html, name="home"),
    path("seats/<int:movie_id>/", views.seat_booking_html, name="seat_booking"),
    path(
        "seats/book/<int:movie_id>/<int:seat_id>/",
        views.process_booking,
        name="book_selected_seat",
    ),
    path("times/<int:movie_id>/", views.movie_time_html, name="movie_time"),
    path("bookings/", views.booking_history_html, name="booking_history"),
    path("cancel/<int:booking_id>/", views.cancel_booking_html, name="cancel_booking"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.signup_html, name="signup"),
    # API
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
