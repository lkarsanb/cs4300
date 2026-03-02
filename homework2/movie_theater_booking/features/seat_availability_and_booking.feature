Feature: Seat Availability and Booking
    Scenario: User can view the available times and dates for a movie
        Given I am on the movie "times" page for "Black Panther"
        When I select the available date "May 20, 2026"
        Then I should see "8:00" is an available time

    Scenario: User can select a day and time to see available seats
        Given I am on the movie "times" page for "Black Panther"
        When I select the available date "May 20, 2026"
        And I select "8:00"
        Then I should be redirected to the "seats" page

    Scenario: User can click on a seat to book it if they are signed in
        Given I am signed in
        And I am on the "seats" page for "Black Panther" on "May 20, 2026" at "8:00"
        When I select seat "C3" which is available
        Then the seat should be booked
        And I should be redirected to the bookings page

    Scenario: User can click on a seat and be redirected to sign in if not already to book seat
        Given I am not signed in
        And I am on the "seats" page for "Black Panther" on "May 20, 2026" at "8:00"
        When I select seat "C3" which is available
        Then I should be redirected to the "log in" page

    Scenario: User cannot book unavailable seat
        Given I am signed in
        And I am on the "seats" page for "Black Panther" on "May 20, 2026" at "8:00"
        When I select seat "A1" which is already booked
        Then I cannot book the seat