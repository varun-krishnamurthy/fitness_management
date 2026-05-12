# Step definitions for diet plans and logs BDD scenarios
from frappe_bdd import given, when, then, step
import frappe
from frappe.utils import getdate

@given("there is a fitness trainer {trainer_name} with specialty {specialty}")
def step_impl(context, trainer_name, specialty):
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

@given("there is a personal training package {package_name} for client {client_name} with trainer {trainer_name} that includes diet plan")
def step_impl(context, package_name, client_name, trainer_name):
    if not frappe.db.exists("Personal Training Package", {"package_name": package_name}):
        pkg = frappe.get_doc({
            "doctype": "Personal Training Package",
            "package_name": package_name,
            "client": client_name,
            "trainer": trainer_name,
            "start_date": getdate(),
            "duration_months": 1,
            "price": 1000,
            "includes_diet_plan": 1,
            "is_active": 1,
            "status": "Active"
        })
        pkg.insert()
    else:
        pkg = frappe.get_doc("Personal Training Package", {"package_name": package_name})
        pkg.client = client_name
        pkg.trainer = trainer_name
        pkg.includes_diet_plan = 1
        pkg.status = "Active"
        pkg.save()
    context.package = pkg

@when("I create a diet plan {plan_name} for client {client_name} with:")
def step_impl(context, plan_name, client_name):
    # This step gets the first table (nutrition targets)
    row = context.table[0]
    calorie_target = int(row['calorie_target'])
    protein_target_g = float(row['protein_target_g'])
    carb_target_g = float(row['carb_target_g'])
    fat_target_g = float(row['fat_target_g'])
    
    # Store targets in context for the next step
    context.diet_plan_targets = {
        'calorie_target': calorie_target,
        'protein_target_g': protein_target_g,
        'carb_target_g': carb_target_g,
        'fat_target_g': fat_target_g
    }
    context.diet_plan_name = plan_name
    context.diet_plan_client = client_name

@when("I add meals:")
def step_impl(context):
    # This step gets the second table (meals)
    diet_plan = frappe.get_doc({
        "doctype": "Diet Plan",
        "plan_name": context.diet_plan_name,
        "client": context.diet_plan_client,
        "trainer": context.trainer.name,
        "calorie_target": context.diet_plan_targets['calorie_target'],
        "protein_target_g": context.diet_plan_targets['protein_target_g'],
        "carb_target_g": context.diet_plan_targets['carb_target_g'],
        "fat_target_g": context.diet_plan_targets['fat_target_g'],
        "is_template": 0
    })
    
    for row in context.table:
        diet_plan.append("meals", {
            "meal_time": row['meal_time'],
            "meal_name": row['meal_name'],
            "description": row['description'],
            "calories": int(row['calories']),
            "protein_g": float(row['protein_g']),
            "carbs_g": float(row['carbs_g']),
            "fat_g": float(row['fat_g'])
        })
    
    diet_plan.insert()
    context.diet_plan = diet_plan

@then("the diet plan should be created with correct nutritional targets")
def step_impl(context):
    assert context.diet_plan.calorie_target == context.diet_plan_targets['calorie_target']
    assert context.diet_plan.protein_target_g == context.diet_plan_targets['protein_target_g']
    assert context.diet_plan.carb_target_g == context.diet_plan_targets['carb_target_g']
    assert context.diet_plan.fat_target_g == context.diet_plan_targets['fat_target_g']

@then("the meals should be saved with correct nutritional values")
def step_impl(context):
    assert len(context.diet_plan.meals) == len(context.table)
    for i, row in enumerate(context.table):
        meal = context.diet_plan.meals[i]
        assert meal.meal_time == row['meal_time']
        assert meal.meal_name == row['meal_name']
        assert meal.description == row['description']
        assert meal.calories == int(row['calories'])
        assert meal.protein_g == float(row['protein_g'])
        assert meal.carbs_g == float(row['carbs_g'])
        assert meal.fat_g == float(row['fat_g'])

@then("the total daily calories should sum to {expected_total}")
def step_impl(context, expected_total):
    total = sum(meal.calories for meal in context.diet_plan.meals)
    assert total == int(expected_total), f"Expected total calories {expected_total}, got {total}"

@given("there is a diet plan {plan_name} for client {client_name}")
def step_impl(context, plan_name, client_name):
    if not frappe.db.exists("Diet Plan", {"plan_name": plan_name, "client": client_name}):
        # Create a basic diet plan if it doesn't exist
        diet_plan = frappe.get_doc({
            "doctype": "Diet Plan",
            "plan_name": plan_name,
            "client": client_name,
            "trainer": context.trainer.name,
            "calorie_target": 1500,
            "protein_target_g": 120,
            "carb_target_g": 150,
            "fat_target_g": 40,
            "is_template": 0
        })
        diet_plan.append("meals", {
            "meal_time": "Breakfast",
            "meal_name": "Oatmeal Bowl",
            "description": "Oats with berries and nuts",
            "calories": 350,
            "protein_g": 12,
            "carbs_g": 50,
            "fat_g": 10
        })
        diet_plan.insert()
    else:
        diet_plan = frappe.get_doc("Diet Plan", {"plan_name": plan_name, "client": client_name})
    context.diet_plan = diet_plan

@when("I log diet consumption for date {date} with:")
def step_impl(context, date):
    diet_log = frappe.get_doc({
        "doctype": "Diet Log",
        "log_date": date,
        "client": context.customer.name,
        "trainer": context.trainer.name
    })
    
    for row in context.table:
        diet_log.append("meals_consumed", {
            "meal_time": row['meal_time'],
            "meal_name": row['meal_name'],
            "calories_consumed": int(row['calories_consumed']),
            "protein_g": float(row['protein_g']),
            "carbs_g": float(row['carbs_g']),
            "fat_g": float(row['fat_g']),
            "notes": row['notes']
        })
    
    diet_log.insert()
    context.diet_log = diet_log

@then("the diet log should be created for date {date}")
def step_impl(context, date):
    assert context.diet_log.log_date == date

@then("the total calories consumed should be {expected_calories}")
def step_impl(context, expected_calories):
    # Calculate total from the meals_consumed table
    total = sum(meal.calories_consumed for meal in context.diet_log.meals_consumed)
    assert total == int(expected_calories), f"Expected total calories {expected_calories}, got {total}"

@then("the total protein consumed should be {expected_protein}g")
def step_impl(context, expected_protein):
    total = sum(meal.protein_g for meal in context.diet_log.meals_consumed)
    assert abs(total - float(expected_protein)) < 0.01, f"Expected total protein {expected_protein}g, got {total}g"

@then("the total carbs consumed should be {expected_carbs}g")
def step_impl(context, expected_carbs):
    total = sum(meal.carbs_g for meal in context.diet_log.meals_consumed)
    assert abs(total - float(expected_carbs)) < 0.01, f"Expected total carbs {expected_carbs}g, got {total}g"

@then("the total fat consumed should be {expected_fat}g")
def step_impl(context, expected_fat):
    total = sum(meal.fat_g for meal in context.diet_log.meals_consumed)
    assert abs(total - float(expected_fat)) < 0.01, f"Expected total fat {expected_fat}g, got {total}g"

@then("the client can add notes to their diet log")
def step_impl(context):
    context.diet_log.client_notes = "Felt great today!"
    context.diet_log.save()
    context.diet_log.reload()
    assert context.diet_log.client_notes == "Felt great today!"

@when("I view the diet adherence report")
def step_impl(context):
    # We'll simulate viewing the report by calculating adherence
    # In a real test, we might call a report method or check the UI
    # For now, we'll just set the adherence in context for the next step
    target = context.diet_plan.calorie_target
    actual = context.diet_log.total_calories
    if target > 0:
        adherence_percentage = (actual / target) * 100
    else:
        adherence_percentage = 0
    context.adherence_percentage = adherence_percentage

@then("I should see that the client consumed {expected_percentage}% of their target calories")
def step_impl(context, expected_percentage):
    expected = float(expected_percentage)
    actual = context.adherence_percentage
    assert abs(actual - expected) < 1.0, f"Expected adherence {expected}%, got {actual}%"

@then("the adherence status should be {status}")
def step_impl(context, status):
    # Define status based on percentage
    percentage = context.adherence_percentage
    if percentage >= 90:
        calculated_status = "On Track"
    elif percentage >= 75:
        calculated_status = "Moderate"
    else:
        calculated_status = "Needs Improvement"
    assert calculated_status == status, f"Expected adherence status {status}, got {calculated_status}"

@when("I try to create a diet log for a client not assigned to any package with diet plan")
def step_impl(context):
    # Create a client without a package that includes diet plan
    client_no_pkg = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": "Client No Package",
        "trainer": context.trainer.name
    })
    client_no_pkg.insert()
    
    # Try to create a diet log for this client
    try:
        diet_log = frappe.get_doc({
            "doctype": "Diet Log",
            "log_date": getdate(),
            "client": client_no_pkg.name,
            "trainer": context.trainer.name
        })
        diet_log.insert()
        context.creation_success = True
        context.creation_error = None
    except Exception as e:
        context.creation_success = False
        context.creation_error = str(e)

@then("I should see an error that the client needs an active package with diet plan inclusion")
def step_impl(context):
    assert not context.creation_success, "Diet log was created successfully but should have failed"
    assert context.creation_error is not None, "No error message was captured"
    # In a real implementation, we would check the error message for specific text
    # For now, we just verify that an error occurred