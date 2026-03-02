Feature: Booking History
    Scenario: A user that is logged-in can view their booking history
        Given I am signed in to my account
        And I have a booking for "Black Panther"
        When I view my booking history
        Then I should see "Black Panther" in the list

    Scenario: A user can delete bookings they have made
        Given I am signed in to my account
        And I am on the bookings page
        And I have a booking for "Black Panther"
        Then I can delete the booking
        Then "Black Panther" will no longer be shown on my booking history