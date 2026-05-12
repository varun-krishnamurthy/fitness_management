# Fitness Management App for Personal Trainers

This app extends ERPNext to manage fitness training businesses.

## Features

- Extended Customer and Employee with fitness-specific fields
- Personal Training Package management (as a separate DocType, designed to be integrated with Subscription in the future)
- Workout Program and Session tracking
- Diet Plan and Logging
- Payment Transaction processing
- Automation and reminders
- Role-based access control

## Installation

bench --site your-site install-app fitness_management
bench --site your-site migrate

## Notes on Subscription

The Personal Training Package DocType is currently implemented as a standalone DocType for simplicity.
However, it is designed to be easily integrated with ERPNext's Subscription and Subscription Plan DocTypes.
Future versions may refactor it to use those built-in DocTypes.

## Documentation

- [Solution Document](SOLUTION.md)
- [Test Strategy](TEST_STRATEGY.md)
- [Implementation Summary](SUMMARY.md)
