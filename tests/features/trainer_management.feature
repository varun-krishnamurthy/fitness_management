Feature: Trainer Management
  As a fitness studio manager
  I want to manage trainers and their specialties
  So that I can assign clients to the right trainers

  Background:
    Given there is an employee record for "John Trainer"
    And there is an employee record for "Jane Trainer"

  Scenario: Mark an employee as a fitness trainer
    When I update the employee "John Trainer" to set:
      | is_fitness_trainer | 1 |
      | trainer_specialty  | Strength Training |
      | certifications     | NASM-CPT, CPR/AED |
      | hourly_rate        | 50.00 |
    Then the employee "John Trainer" should be marked as a fitness trainer
    And the trainer specialty should be "Strength Training"
    And the certifications should be set
    And the hourly rate should be 50.00

  Scenario: Validate trainer specialty options
    When I try to set the trainer_specialty to "Invalid Specialty" for employee "John Trainer"
    Then I should see an error that the trainer specialty must be one of the allowed options
    And the specialty should not be saved

  Scenario: Assign trainer to customer
    Given there is a customer "Jane Client"
    When I update the customer "Jane Client" to set the trainer to "John Trainer"
    Then the customer "Jane Client" should have trainer "John Trainer"
    And the trainer field should be read-only after assignment (unless changed by manager)

  Scenario: List trainers by specialty
    Given there are two fitness trainers:
      | trainer_name   | specialty           |
      | John Trainer   | Strength Training   |
      | Jane Trainer   | Yoga                |
    When I filter trainers by specialty "Yoga"
    Then I should see only "Jane Trainer" in the list
    And the count should be 1

  Scenario: Trainer cannot be deleted if they have active clients
    Given there is a fitness trainer "John Trainer"
    And there is a customer "Jane Client" assigned to trainer "John Trainer"
    And there is an active personal training package for client "Jane Client" with trainer "John Trainer"
    When I try to delete the employee "John Trainer"
    Then I should see an error that the trainer cannot be deleted because they have active clients
    And the trainer record should not be deleted