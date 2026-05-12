Feature: Payment Processing for Fitness Packages
  As a fitness studio manager
  I want to process payments for personal training packages
  So that I can track revenue and client commitments

  Background:
    Given there is a customer "Jane Client"
    And there is a fitness trainer "John Trainer"
    And there is a personal training package "Premium Fitness" priced at $500 for 3 months
    And payment gateway settings are configured for Razorpay in test mode

  Scenario: Process successful payment for a package
    When I create a payment transaction for client "Jane Client" for package "Premium Fitness" of $500 via Razorpay
    And the payment gateway returns success
    Then the payment transaction status should be "Success"
    And a payment receipt should be generated
    And the personal training package should remain in "Active" status

  Scenario: Handle failed payment
    When I create a payment transaction for client "Jane Client" for package "Premium Fitness" of $500 via Razorpay
    And the payment gateway returns failure due to insufficient funds
    Then the payment transaction status should be "Failed"
    And the personal training package should remain in draft or inactive status
    And the client should be notified of payment failure

  Scenario: Process refund for a package
    Given there is a successful payment transaction of $500 for package "Premium Fitness"
    When I initiate a refund of $500 for the payment transaction
    And the payment gateway processes the refund successfully
    Then the payment transaction status should be "Refunded"
    And the personal training package status should be updated to "Cancelled" or appropriate
    And a refund receipt should be generated

  Scenario: Validate payment amount matches package price
    Given there is a personal training package "Premium Fitness" priced at $500
    When I try to process a payment of $400 for this package
    Then I should see a warning that the payment amount does not match the package price
    But I can still process the payment (for partial payments or deposits)

  Scenario: Handle payment in different currency
    Given there is a personal training package "International Client Package" priced at $500 USD
    And the client's preferred currency is USD
    When I process a payment of $500 USD
    Then the payment transaction should record currency as USD
    And the amount should be correctly converted if base currency is different

  Scenario: Webhook handles payment status updates
    Given there is a payment transaction in "Pending" status
    When the payment gateway webhook notifies of payment success
    Then the payment transaction status should be updated to "Success"
    And any linked Sales Invoice should be marked as paid
    And appropriate notifications should be sent