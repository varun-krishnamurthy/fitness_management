Feature: Client Portal Access
  As a fitness client
  I want to view my training packages, workout sessions, and diet plans via the client portal
  So that I can stay informed about my fitness journey

  Background:
    Given there is a fitness trainer "John Trainer"
    And there is a customer "Jane Client" assigned to trainer "John Trainer"
    And there is a personal training package "Strength Builder" for client "Jane Client" with trainer "John Trainer"
    And there is a workout session scheduled for client "Jane Client" on "2026-05-15" at "10:00"
    And there is a diet plan "Weight Loss Plan" for client "Jane Client"

  Scenario: Client logs in to the portal
    When the client "Jane Client" logs into the client portal with valid credentials
    Then the client should see their dashboard
    And the dashboard should show their active packages
    And the dashboard should show upcoming workout sessions

  Scenario: Client views their personal training package
    Given the client "Jane Client" is logged into the client portal
    When the client navigates to "My Packages"
    Then the client should see their "Strength Builder" package
    And the package should show status "Active"
    And the package should show start and end dates
    And the package should show assigned trainer "John Trainer"

  Scenario: Client views upcoming workout sessions
    Given the client "Jane Client" is logged into the client portal
    When the client navigates to "My Workouts"
    Then the client should see their upcoming workout session on "2026-05-15" at "10:00"
    And the session should show status "Planned"
    And the client can add feedback after the session is completed

  Scenario: Client views their diet plan
    Given the client "Jane Client" is logged into the client portal
    When the client navigates to "My Diet Plans"
    Then the client should see their "Weight Loss Plan"
    And the diet plan should show nutritional targets
    And the client can view meal details

  Scenario: Client logs a workout session (if enabled)
    Given the client "Jane Client" has completed a workout session
    When the client logs into the client portal and navigates to "Log Workout"
    And the client selects the session from "2026-05-15" at "10:00"
    And the client logs:
      | exercise_name | sets_completed | reps_completed | weight_used | rpe |
      | Bench Press   | 3              | 10             | 60          | 8   |
      | Squats        | 3              | 12             | 80          | 9   |
    Then the workout session should be updated with the logged exercises
    And the session status should remain as completed (or update if it was planned)
    And the trainer should be able to see the client's logged data

  Scenario: Client logs diet consumption
    Given the client "Jane Client" is logged into the client portal
    When the client navigates to "Log Diet" for date "2026-05-15"
    And the client logs:
      | meal_time       | meal_name        | calories_consumed | protein_g | carbs_g | fat_g |
      | Breakfast       | Oatmeal Bowl     | 350               | 12        | 50      | 10    |
      | Lunch           | Grilled Chicken Salad | 400             | 35        | 20      | 15    |
      | Dinner          | Baked Salmon     | 450               | 40        | 30      | 15    |
      | Snack           | Greek Yogurt     | 150               | 15        | 20      | 3     |
    Then the diet log should be created for date "2026-05-15"
    And the total calories should be 1350
    And the trainer should be able to see the client's logged diet

  Scenario: Client views payment history
    Given the client "Jane Client" has made a payment of $300 for package "Strength Builder"
    When the client logs into the client portal and navigates to "Payment History"
    Then the client should see their payment of $300
    And the payment should show status "Success"
    And the payment should show date and transaction ID

  Scenario: Client cannot access other clients' data
    Given there is another customer "John Client" with their own package
    When the client "Jane Client" logs into the client portal
    Then the client "Jane Client" should not see any data for "John Client"
    And the client "Jane Client" should only see their own packages, workouts, and diets