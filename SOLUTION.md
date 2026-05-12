# Solution Document for Fitness Management App

## Problem Statement
Personal trainers need a comprehensive system to manage clients, workout programs, diet plans, and payments. Existing ERPNext modules do not cover fitness-specific workflows out-of-the-box.

## Solution Approach
We will create a new Frappe app called `fitness_management` that extends core ERPNext DocTypes (Customer, Employee) and introduces new DocTypes for fitness management. The app will integrate with a payment gateway (Razorpay example) for subscription and package payments.

## Modules
- Fitness Management

## DocTypes

### 1. Extended DocTypes (via Custom Fields and Hooks)
#### Customer (extend)
- Add custom fields:
  - `date_of_birth` (Date)
  - `gender` (Select: Male, Female, Other)
  - `fitness_goals` (Small Text)
  - `emergency_contact` (Data)
  - `emergency_phone` (Phone)
  - `trainer` (Link to Employee, filtered by trainer role)

#### Employee (extend)
- Add custom fields:
  - `trainer_specialty` (Select: Strength Training, Yoga, Cardio, Rehabilitation, etc.)
  - `certifications` (Small Text)
  - `is_fitness_trainer` (Check, default 0)
  - `hourly_rate` (Currency)

### 2. New DocTypes
#### Personal Training Package
- `package_name` (Data, required)
- `description` (Long Text)
- `duration_months` (Int, required)
- `sessions_per_week` (Int)
- `price` (Currency, required)
- `currency` (Link to Currency, default INR)
- `includes_workout_plan` (Check)
- `includes_diet_plan` (Check)
- `is_active` (Check, default 1)
- `trainer` (Link to Employee, required, filtered by is_fitness_trainer=1)
- `client` (Link to Customer, required)
- `start_date` (Date, required)
- `end_date` (Date, computed: start_date + duration_months)
- `status` (Select: Active, Expired, Cancelled, Completed)

#### Workout Program
- `program_name` (Data, required)
- `description` (Long Text)
- `trainer` (Link to Employee, required, filtered by is_fitness_trainer=1)
- `target_muscle_groups` (MultiSelect: Chest, Back, Legs, Shoulders, Arms, Core)
- `difficulty_level` (Select: Beginner, Intermediate, Advanced)
- `is_template` (Check, default 0)  # If template, can be reused for multiple clients
- `exercises` (Table: Exercise Item)
  - `exercise_name` (Data)
  - `sets` (Int)
  - `reps` (Int)
  - `weight` (Float, optional)
  - `rest_seconds` (Int)
  - `notes` (Small Text)

#### Workout Session
- `session_date` (Date, required)
- `session_time` (Time, required)
- `client` (Link to Customer, required)
- `trainer` (Link to Employee, required, auto-filled from client's package trainer)
- `package` (Link to Personal Training Package, optional, for validation)
- `workout_program` (Link to Workout Program, optional)
- `exercises_performed` (Table: Exercise Log)
  - `exercise_name` (Data, from program)
  - `sets_completed` (Int)
  - `reps_completed` (Int)
  - `weight_used` (Float)
  - `rpe` (Int, 1-10 Scale)  # Rate of Perceived Exertion
  - `notes` (Small Text)
- `status` (Select: Planned, Completed, Cancelled, No Show)
- `trainer_notes` (Long Text)
- `client_feedback` (Small Text)

#### Diet Plan
- `plan_name` (Data, required)
- `description` (Long Text)
- `trainer` (Link to Employee, required, filtered by is_fitness_trainer=1)
- `calorie_target` (Int)
- `protein_target_g` (Float)
- `carb_target_g` (Float)
- `fat_target_g` (Float)
- `is_template` (Check, default 0)
- `meals` (Table: Meal Item)
  - `meal_time` (Select: Breakfast, Lunch, Dinner, Snack, Pre-Workout, Post-Workout)
  - `meal_name` (Data)
  - `description` (Small Text)
  - `calories` (Int)
  - `protein_g` (Float)
  - `carbs_g` (Float)
  - `fat_g` (Float)

#### Diet Log
- `log_date` (Date, required)
- `client` (Link to Customer, required)
- `trainer` (Link to Employee, required, auto-filled from client's package trainer)
- `diet_plan` (Link to Diet Plan, optional)
- `meals_consumed` (Table: Meal Log)
  - `meal_time` (Select)
  - `meal_name` (Data)
  - `calories_consumed` (Int)
  - `protein_g` (Float)
  - `carbs_g` (Float)
  - `fat_g` (Float)
  - `notes` (Small Text)
- `total_calories` (Int, read-only, calculated)
- `total_protein_g` (Float, read-only)
- `total_carbs_g` (Float, read_only)
- `total_fat_g` (Float, read_only)
- `client_notes` (Small Text)
- `trainer_feedback` (Small Text)

#### Payment Transaction
- `transaction_id` (Data, required, unique)
- `client` (Link to Customer, required)
- `package` (Link to Personal Training Package, optional)
- `amount` (Currency, required)
- `currency` (Link to Currency, default INR)
- `payment_gateway` (Select: Razorpay, Stripe, PayPal, Manual)
- `gateway_transaction_id` (Data)
- `payment_date` (Datetime, required)
- `status` (Select: Pending, Success, Failed, Refunded)
- `payment_method` (Data: Credit Card, UPI, Net Banking, etc.)
- `invoice` (Link to Sales Invoice, optional)  # If we generate an invoice
- `notes` (Small Text)

#### Payment Gateway Settings (Singleton)
- `gateway_name` (Select: Razorpay, Stripe, PayPal)
- `api_key` (Password)
- `api_secret` (Password)
- `webhook_secret` (Password)
- `is_active` (Check, default 1)
- `test_mode` (Check, default 1)

## Integrations
### Payment Gateway
- We will integrate with Razorpay (configurable) for processing package payments.
- On successful payment, create a Payment Transaction record and optionally generate a Sales Invoice.
- Webhook endpoint to verify payment status and update records.

### Automation
- Scheduler events:
  - Daily: Check for expired packages and update status.
  - Daily: Send workout/diet reminders for upcoming sessions.
- DocType events:
  - On submitting a Personal Training Package: Create initial Workout Program and Diet Plan if flags are set.
  - On submitting a Workout Session: Update client progress metrics (optional).

## Security & Permissions
- Roles:
  - `Fitness Manager`: Access to all DocTypes.
  - `Fitness Trainer`: Access to their clients' packages, workout sessions, diet logs; can create programs/plans.
  - `Fitness Client` (Website User): Read-only access to their own packages, sessions, logs via portal.
- Field-level permissions: Sensitive fields (like payment details) restricted to Manager/Trainer.

## Reports
- Package Revenue Report
- Trainer Utilization Report
- Client Progress Tracking (weight, measurements - optional extension)
- Attendance Report (Workout Sessions)
- Diet Adherence Report

## Implementation Notes
- UI is auto-generated from DocType JSON; no custom desk views needed.
- Client portal can be enabled for clients to view their plans and log workouts/diets.
- Print formats for workout sheets and diet charts can be configured.
- All standard Frappe features (naming series, search, filters, export) apply out-of-the-box.

## Files to be Generated
After finalizing this design, the Developer will generate:
- `fitness_management/fitness_management/hooks.py`
- `fitness_management/fitness_management/modules.txt` (contains: "Fitness Management")
- DocType folders under `fitness_management/fitness_management/doctype/` for each DocType listed above (JSON, PY, JS)
- Custom field fixtures for Customer and Employee extensions in `custom_fields/*.json`
- Payment gateway integration server scripts
- Scheduler event definitions
- Basic unit and integration tests (via Test Architect)

## Next Steps
1. Test Architect to review SOLUTION.md and create test strategy.
2. Developer to scaffold app and implement DocTypes.
3. Technical Writer to create user guide.
4. Reviewer to verify code quality.
5. Release Manager to version and release.

---
*Design approved by Architect persona. Ready for Test Architect phase.*