Feature: Workout Session Management
  As a fitness trainer
  I want to manage workout sessions for clients
  So that I can track training progress and attendance

  Background:
    Given there is a fitness trainer "John Trainer" with specialty "Strength Training"
    And there is a customer "Jane Client" assigned to trainer "John Trainer"
    And there is a personal training package "Strength Builder" for client "Jane Client" with trainer "John Trainer"
    And there is a workout program "Beginner Strength" created by trainer "John Trainer"

  Scenario: Schedule a workout session
    When I schedule a workout session for client "Jane Client" on "2026-05-15" at "10:00"
    Then the workout session should be created with status "Planned"
    And the session should be linked to client "Jane Client"
    And the session should be linked to trainer "John Trainer"

  Scenario: Complete a workout session
    Given there is a planned workout session for client "Jane Client" on "2026-05-15" at "10:00"
    When I complete the workout session with:
      | exercise_name | sets_completed | reps_completed | weight_used | rpe |
      | Bench Press   | 3              | 10             | 60          | 8   |
      | Squats        | 3              | 12             | 80          | 9   |
    Then the workout session status should be "Completed"
    And the exercises performed should be recorded correctly
    And the trainer can add notes to the session

  Scenario: Cancel a workout session
    Given there is a planned workout session for client "Jane Client" on "2026-05-15" at "10:00"
    When I cancel the workout session
    Then the workout session status should be "Cancelled"
    And the session should not be counted in attendance reports

  Scenario: Mark client as no-show
    Given there is a planned workout session for client "Jane Client" on "2026-05-15" at "10:00"
    When I mark the client as no-show for the session
    Then the workout session status should be "No Show"
    And the trainer can add notes about the no-show

  Scenario: Validate session belongs to client's package
    Given there is a personal training package "Strength Builder" for client "Jane Client" with 3 sessions per week
    And there are 3 workout sessions already scheduled for this week
    When I try to schedule a fourth workout session for the same week
    Then I should see a warning about exceeding weekly sessions limit
    But I can still schedule the session (soft limit)