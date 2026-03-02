from django.contrib import admin, messages
from .models import Movie, Seat, Booking
# Register your models here.

admin.site.register(Movie)
admin.site.register(Booking)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    actions = ["generate_seats"]

    @admin.action(description="Generate seats automatically")
    def generate_seats(self, request, queryset):
        """
        Action function that allows admin to easily add seats for all 5 theaters which are assumed to have rows A-F and
        columns 1-6.
        :param request: HTTP request that represents the current request.
        :param queryset: The seat objects selected for the action to perform on.
        """

        seat_rows = ["A", "B", "C", "D", "E", "F"]
        seat_cols = [1, 2, 3, 4, 5, 6]

        for seat_obj in queryset:
            for row in seat_rows:
                for col in seat_cols:
                    # User get_or_create to prevent duplicates if admin selects option more than once.
                    Seat.objects.get_or_create(
                        movie=seat_obj.movie,
                        movie_location=seat_obj.movie_location,
                        movie_time=seat_obj.movie_time,
                        seat_row=row,
                        seat_col=col
                    )
        self.message_user(request, f"Seats generated successfully.", messages.SUCCESS)