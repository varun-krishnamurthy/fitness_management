Feature: Personal Training Package Management
  As a fitness studio manager
  I want to create and manage personal training packages for clients
  So that I can sell training programs and track client commitments

  Background:
    Given there is a fitness trainer "John Trainer"
    And there is a customer "Jane Client"

  Scenario: Create a personal training package
    When I create a personal training package "Strength Builder" for client "Jane Client" with:
      | trainer        | duration_months | sessions_per_week | price | includes_workout_plan | includes_diet_plan |
      | John Trainer   | 3               | 3                 | 300   | 1                     | 0                  |
    And I set the start date to "2026-05-01"
    Then the package should be created with status "Active"
    And the end date should be calculated as "2026-08-01"
    And the client "Jane Client" should be linked to the package
    And the trainer "John Trainer" should be linked as the trainer

  Scenario: Activate a package from draft
    Given there is a personal training package "Strength Builder" for client "Jane Client" in draft status
    When I activate the package
    Then the package status should be "Active"
    And the start date should be set to today if not already set
    And the end date should be calculated accordingly

  Scenario: Expire a package
    Given there is an active personal training package "Strength Builder" for client "Jane Client" with end date "2026-05-01"
    When the date reaches "2026-05-02"
    And the daily scheduler runs
    Then the package status should be updated to "Expired"

  Scenario: Cancel a package
    Given there is an active personal training package "Strength Builder" for client "Jane Client"
    When I cancel the package with reason "Client moved away"
    Then the package status should be "Cancelled"
    And the cancellation reason should be recorded
    And no new workout sessions can be scheduled for this package

  Scenario: Complete a package
    Given there is an active personal training package "Strength Builder" for client "Jane Client"
    And all scheduled workout sessions for the package have been completed
    When I mark the package as completed
    Then the package status should be "Completed"
    And the package should no longer be editable

  Scenario: Validate trainer assignment
    Given there is an employee "Jane Trainer" who is not marked as a fitness trainer
    When I try to assign "Jane Trainer" as the trainer for a new package
    Then I should see an error that the selected employee is not a fitness trainer
    And I cannot save the package

  Scenario: Validate package duration
    When I try to create a package with duration_months set to 0
    Then I should see a validation error that duration must be greater than zero
    And the package should not be created