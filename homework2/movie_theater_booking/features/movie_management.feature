Feature: Movie Management
    Scenario: See the available movies
        Given I am on the home page
        And "Avengers: Endgame" is an available movie
        When I select the movie
        Then I am redirected to the information page
        And I can see the movie's duration is "181 minutes"

    Scenario: Admin can add a new movie
        Given I am logged in as an administrator
        When I create a new movie "Finding Nemo"
        Then the movie "Finding Nemo" should exist in the database
