# Test Strategy for Fitness Management App

## Scope
This test strategy covers the fitness_management Frappe app, including:
- Extended Customer and Employee DocTypes (custom fields)
- New DocTypes: Personal Training Package, Workout Program, Workout Session, Diet Plan, Diet Log, Payment Transaction, Payment Gateway Settings
- Integrations: Payment gateway (Razorpay)
- Automation: Scheduler events, DocType events
- Security: Roles and permissions
- Reports: Package revenue, trainer utilization, client progress, attendance, diet adherence

## Test Levels

### 1. Unit Testing
- **Target**: Python controllers, utility functions, helper methods
- **Framework**: Frappe's built-in unit testing (using `unittest`)
- **Coverage**: 
  - Validation logic in DocType controllers (e.g., date calculations, field constraints)
  - Methods in hooks.py (scheduler events, doc_events)
  - Payment gateway integration utilities
  - Custom field extension logic
- **Tools**: 
  - `frappe.utils` for mocking
  - `unittest.mock` for patching external calls (e.g., Razorpay API)

### 2. Integration Testing
- **Target**: DocType lifecycle, multi-DocType workflows, server-side scripts
- **Framework**: Frappe integration tests (using `frappe.tests.utils`)
- **Coverage**:
  - DocType creation, submission, cancellation workflows
  - Cross-DocType validation (e.g., linking workout sessions to packages)
  - Scheduler event execution (expired package status update)
  - DocType event triggers (auto-creation of workout/diet plans on package submission)
  - Payment transaction creation and status updates
  - Role-based permission enforcement
- **Setup**: 
  - Install app in test site
  - Create necessary dependency data (Currency, Employee, Customer records)
  - Mock external payment gateway calls

### 3. Behavior-Driven Development (BDD) Acceptance Testing
- **Framework**: Behave (via `frappe` BDD support) with Gherkin syntax
- **Feature Files**: Located in `tests/features/`
- **Coverage**:
  - Happy path scenarios for core user journeys
  - Edge cases (invalid inputs, boundary conditions)
  - Error cases (gateway failures, validation errors)
  - Security scenarios (unauthorized access attempts)
- **Execution**: 
  - Use Frappe's test browser simulation
  - Run against a test site with realistic data

## Test Environment
- **Site**: Dedicated test site (e.g., `test_fitness_management`)
- **Dependencies**: 
  - Frappe framework
  - ERPNext (for Customer, Employee, Currency DocTypes)
  - mock libraries for external services
- **Data**: 
  - Fixture data for standard ERPNext setup
  - Custom fixtures for fitness-specific master data (exercise templates, meal templates)

## Acceptance Criteria
Each user story from SOLUTION.md must have:
- At least one BDD scenario in Gherkin format
- Corresponding unit tests for critical logic
- Integration tests for workflow validation
- Pass rate of 100% on test site before release

## Test Data Management
- **Fixtures**: 
  - Standard ERPNext fixtures (Currency, Country, etc.)
  - Custom fixtures for fitness app (exercise lists, meal databases, trainer specialties)
- **Factories**: 
  - Use Factory Boy pattern for generating test data in Python tests
  - Gherkin steps for creating test data in BDD scenarios
- **Isolation**: 
  - Each test scenario cleans up after itself
  - Use transactions rollback where possible

## Non-Functional Testing
- **Performance**: 
  - Load testing for package creation and session logging (target: <2s response time)
  - Database query optimization checks (indexes on frequently queried fields)
- **Security**: 
  - Penetration testing for payment data handling
  - Input validation and sanitization verification
  - Role-based access control testing
- **Usability**: 
  - Form validation and user feedback checks
  - Mobile responsiveness of auto-generated Frappe forms

## Test Execution Plan
1. **Unit Tests**: Run on every code commit
2. **Integration Tests**: Run on every code commit and nightly
3. **BDD Scenarios**: 
   - Run on feature branch completion
   - Run nightly on test environment
   - Run before release to staging
4. **Coverage Targets**:
   - Unit test coverage: >80% for controllers and hooks
   - Integration test coverage: >70% for critical workflows
   - BDD coverage: 100% of acceptance criteria

## Tools and Frameworks
- **Unit/Integration**: 
  - `frappe.test_runner`
  - `unittest`
  - `mock`
- **BDD**: 
  - `behave` (via Frappe's BDD support)
  - Gherkin syntax
- **Reporting**: 
  - JUnit XML reports for CI integration
  - HTML coverage reports
- **CI Integration**: 
  - GitHub Actions workflow to run tests on pull requests
  - Automatic deployment to test environment on merge to main

## Deliverables
1. TEST_STRATEGY.md (this document)
2. Gherkin feature files in `tests/features/`:
   - workout_sessions.feature
   - diet_plans.feature
   - payments.feature
   - packages.feature
   - trainer_management.feature
   - client_portal.feature
3. Step definition Python files for BDD scenarios
4. Test data fixtures and factories
5. Unit test files for each DocType controller
6. Integration test files for workflows
7. Configuration for test site setup

## Exit Criteria
- All unit tests pass
- All integration tests pass
- All BDD scenarios pass (no `# Status: SKELETON` markers)
- Test coverage meets minimum thresholds
- Security and performance benchmarks met
- Test documentation complete and reviewed

---
*Test Strategy document created by Test Architect persona. Ready for Developer to implement tests and code.*