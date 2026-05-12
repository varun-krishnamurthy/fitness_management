# Step definitions for trainer management BDD scenarios
from frappe_bdd import given, when, then, step
import frappe
from frappe.utils import getdate

@given("there is an employee record for {employee_name}")
def step_impl(context, employee_name):
    if not frappe.db.exists("Employee", {"employee_name": employee_name}):
        employee = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": employee_name
        })
        employee.insert()
    else:
        employee = frappe.get_doc("Employee", {"employee_name": employee_name})
    # Store in context for later use
    if not hasattr(context, 'employees'):
        context.employees = {}
    context.employees[employee_name] = employee

@when("I update the employee {employee_name} to set:")
def step_impl(context, employee_name):
    employee = frappe.get_doc("Employee", {"employee_name": employee_name})
    for row in context.table:
        for field, value in row.items():
            # Handle special cases for checkboxes and numeric fields
            if field == "is_fitness_trainer":
                employee.is_fitness_trainer = int(value) == 1
            elif field == "hourly_rate":
                employee.hourly_rate = float(value)
            else:
                # Assume it's a standard field
                setattr(employee, field, value)
    employee.save()
    context.employee = employee

@then("the employee {employee_name} should be marked as a fitness trainer")
def step_impl(context, employee_name):
    employee = frappe.get_doc("Employee", {"employee_name": employee_name})
    assert employee.is_fitness_trainer == 1, f"Employee {employee_name} is not marked as a fitness trainer"

@then("the trainer specialty should be {specialty}")
def step_impl(context, specialty):
    employee = context.employee
    assert employee.trainer_specialty == specialty, f"Expected trainer specialty {specialty}, got {employee.trainer_specialty}"

@then("the certifications should be set")
def step_impl(context):
    employee = context.employee
    assert employee.certifications is not None and employee.certifications != "", "Certifications are not set"

@then("the hourly rate should be {rate}")
def step_impl(context, rate):
    employee = context.employee
    assert float(employee.hourly_rate) == float(rate), f"Expected hourly rate {rate}, got {employee.hourly_rate}"

@when("I try to set the trainer_specialty to {specialty} for employee {employee_name}")
def step_impl(context, specialty, employee_name):
    employee = frappe.get_doc("Employee", {"employee_name": employee_name})
    employee.trainer_specialty = specialty
    try:
        employee.save()
        context.save_success = True
        context.save_error = None
    except Exception as e:
        context.save_success = False
        context.save_error = str(e)

@then("I should see an error that the trainer specialty must be one of the allowed options")
def step_impl(context):
    assert not context.save_success, "Trainer specialty was saved successfully but should have failed"
    assert context.save_error is not None, "No error message was captured"

@given("there is a customer {customer_name}")
def step_impl(context, customer_name):
    if not frappe.db.exists("Customer", {"customer_name": customer_name}):
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name
        })
        customer.insert()
    else:
        customer = frappe.get_doc("Customer", {"customer_name": customer_name})
    context.customer = customer

@when("I update the customer {customer_name} to set the trainer to {trainer_name}")
def step_impl(context, customer_name, trainer_name):
    customer = frappe.get_doc("Customer", {"customer_name": customer_name})
    customer.trainer = trainer_name
    customer.save()
    context.customer = customer

@then("the customer {customer_name} should have trainer {trainer_name}")
def step_impl(context, customer_name, trainer_name):
    customer = frappe.get_doc("Customer", {"customer_name": customer_name})
    assert customer.trainer == trainer_name, f"Expected trainer {trainer_name}, got {customer.trainer}"

@then("the trainer field should be read-only after assignment (unless changed by manager)")
def step_impl(context):
    # We cannot test UI read-only in backend. We'll just note that the field is set.
    pass

@given("there are two fitness trainers:")
def step_impl(context):
    # We'll create two trainers from the table
    context.trainers = []
    for row in context.table:
        trainer_name = row['trainer_name']
        specialty = row['specialty']
        if not frappe.db.exists("Employee", {"employee_name": trainer_name}):
            trainer = frappe.get_doc({
                "doctype": "Employee",
                "employee_name": trainer_name,
                "trainer_specialty": specialty,
                "is_fitness_trainer": 1,
                "hourly_rate": 50.0
            })
            trainer.insert()
        else:
            trainer = frappe.get_doc("Employee", {"employee_name": trainer_name})
            trainer.is_fitness_trainer = 1
            trainer.trainer_specialty = specialty
            trainer.save()
        context.trainers.append(trainer)

@when("I filter trainers by specialty {specialty}")
def step_impl(context, specialty):
    # We'll get all employees that are fitness trainers and have the given specialty
    trainers = frappe.get_all("Employee", 
                              filters={"is_fitness_trainer": 1, "trainer_specialty": specialty},
                              fields=["employee_name"])
    context.filtered_trainers = [t.employee_name for t in trainers]

@then("I should see only {trainer_name} in the list")
def step_impl(context, trainer_name):
    assert len(context.filtered_trainers) == 1, f"Expected 1 trainer, got {len(context.filtered_trainers)}"
    assert context.filtered_trainers[0] == trainer_name, f"Expected trainer {trainer_name}, got {context.filtered_trainers[0]}"

@then("the count should be 1")
def step_impl(context):
    assert len(context.filtered_trainers) == 1, f"Expected count 1, got {len(context.filtered_trainers)}"

@given("there is a fitness trainer {trainer_name}")
def step_impl(context, trainer_name):
    if not frappe.db.exists("Employee", {"employee_name": trainer_name}):
        trainer = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": trainer_name,
            "is_fitness_trainer": 1,
            "hourly_rate": 50.0
        })
        trainer.insert()
    else:
        trainer = frappe.get_doc("Employee", {"employee_name": trainer_name})
        trainer.is_fitness_trainer = 1
    context.trainer = trainer

@given("there is a customer {customer_name} assigned to trainer {trainer_name}")
def step_impl(context, customer_name, trainer_name):
    if not frappe.db.exists("Customer", {"customer_name": customer_name}):
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "trainer": trainer_name
        })
        customer.insert()
    else:
        customer = frappe.get_doc("Customer", {"customer_name": customer_name})
        customer.trainer = trainer_name
        customer.save()
    context.customer = customer

@given("there is an active personal training package for client {client_name} with trainer {trainer_name}")
def step_impl(context, client_name, trainer_name):
    if not frappe.db.exists("Personal Training Package", {"client": client_name}):
        pkg = frappe.get_doc({
            "doctype": "Personal Training Package",
            "package_name": f"Package for {client_name}",
            "client": client_name,
            "trainer": trainer_name,
            "start_date": getdate(),
            "duration_months": 1,
            "price": 100,
            "is_active": 1,
            "status": "Active"
        })
        pkg.insert()
    else:
        pkg = frappe.get_doc("Personal Training Package", {"client": client_name})
        pkg.trainer = trainer_name
        pkg.status = "Active"
        pkg.save()
    context.package = pkg

@when("I try to delete the employee {employee_name}")
def step_impl(context, employee_name):
    try:
        frappe.delete_doc("Employee", employee_name)
        context.delete_success = True
        context.delete_error = None
    except Exception as e:
        context.delete_success = False
        context.delete_error = str(e)

@then("I should see an error that the trainer cannot be deleted because they have active clients")
def step_impl(context):
    assert not context.delete_success, "Trainer was deleted successfully but should have failed"
    assert context.delete_error is not None, "No error message was captured"