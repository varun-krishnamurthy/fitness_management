Feature: Diet Plan and Logging Management
  As a fitness trainer
  I want to create diet plans and track client nutrition
  So that I can help clients achieve their dietary goals

  Background:
    Given there is a fitness trainer "John Trainer" with specialty "Nutrition"
    And there is a customer "Jane Client" assigned to trainer "John Trainer"
    And there is a personal training package "Weight Loss Program" for client "Jane Client" with trainer "John Trainer" that includes diet plan

  Scenario: Create a diet plan
    When I create a diet plan "Weight Loss Plan" for client "Jane Client" with:
      | calorie_target | protein_target_g | carb_target_g | fat_target_g |
      | 1500           | 120              | 150           | 40           |
    And I add meals:
      | meal_time       | meal_name        | description                    | calories | protein_g | carbs_g | fat_g |
      | Breakfast       | Oatmeal Bowl     | Oats with berries and nuts     | 350      | 12        | 50      | 10    |
      | Lunch           | Grilled Chicken Salad | Chicken breast with mixed greens | 400      | 35        | 20      | 15    |
      | Dinner          | Baked Salmon     | Salmon with quinoa and vegetables | 450      | 40        | 30      | 15    |
      | Snack           | Greek Yogurt     | Plain Greek yogurt with honey  | 150      | 15        | 20      | 3     |
    Then the diet plan should be created with correct nutritional targets
    And the meals should be saved with correct nutritional values
    And the total daily calories should sum to 1350

  Scenario: Log daily diet consumption
    Given there is a diet plan "Weight Loss Plan" for client "Jane Client"
    When I log diet consumption for date "2026-05-15" with:
      | meal_time       | meal_name        | calories_consumed | protein_g | carbs_g | fat_g | notes               |
      | Breakfast       | Oatmeal Bowl     | 350               | 12        | 50      | 10    |                     |
      | Lunch           | Grilled Chicken Salad | 400             | 35        | 20      | 15    | Added extra chicken |
      | Dinner          | Baked Salmon     | 450               | 40        | 30      | 15    |                     |
      | Snack           | Greek Yogurt     | 150               | 15        | 20      | 3     |                     |
    Then the diet log should be created for date "2026-05-15"
    And the total calories consumed should be 1350
    And the total protein consumed should be 102g
    And the total carbs consumed should be 120g
    And the total fat consumed should be 43g
    And the client can add notes to their diet log

  Scenario: Compare planned vs actual consumption
    Given there is a diet plan "Weight Loss Plan" with target 1500 calories
    And there is a diet log for "2026-05-15" with actual consumption of 1350 calories
    When I view the diet adherence report
    Then I should see that the client consumed 90% of their target calories
    And the adherence status should be "On Track"

  Scenario: Validate diet log belongs to client's package
    Given there is a personal training package "Weight Loss Program" for client "Jane Client"
    When I try to create a diet log for a client not assigned to any package with diet plan
    Then I should see an error that the client needs an active package with diet plan inclusion