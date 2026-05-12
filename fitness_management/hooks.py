# -*- coding: utf-8 -*-
from . import __version__ as app_version

app_name = "fitness_management"
app_title = "Fitness Management"
app_publisher = "Your Name"
app_description = "Fitness Management app for Personal Trainers"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "you@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/fitness_management/css/fitness_management.css"
# app_include_js = "/assets/fitness_management/js/fitness_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/fitness_management/css/fitness_management.css"
# web_include_js = "/assets/fitness_management/js/fitness_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "fitness_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "fitness_management.install.before_install"
# after_install = "fitness_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "fitness_management.uninstall.before_uninstall"
# after_uninstall = "fitness_management.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "fitness_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in desk conditions

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Events
# --------------
# Hook on document methods and events

doc_events = {
	# We can add doc events for our custom DocTypes here if needed
	# Example:
	# "Personal Training Package": {
	# 	"before_insert": "fitness_management.fitness_management.doctype.personal_training_package.personal_training_package.before_insert"
	# }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"fitness_management.tasks.all"
	],
	"daily": [
		"fitness_management.tasks.daily"
	],
	"hourly": [
		"fitness_management.tasks.hourly"
	],
	"weekly": [
		"fitness_management.tasks.weekly"
	],
	"monthly": [
		"fitness_management.tasks.monthly"
	]
}

# Testing
# -------

# before_tests = "fitness_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "fitness_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "fitness_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# --------------
# before_request = "fitness_management.utils.before_request"
# after_request = "fitness_management.utils.after_request"

# Job Events
# ----------
# before_job = "fitness_management.utils.before_job"
# after_job = "fitness_management.utils.after_job"

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"field_name": "field_name",
# 		"field_type": "Date",
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"fitness_management.auth.validate"
# ]

# Fixtures
fixtures = [
	{
		"dt": "Custom Field",
		"filters": [
			[
				"name",
				"in",
				[
					"Customer-date_of_birth",
					"Customer-emergency_contact",
					"Customer-emergency_phone",
					"Customer-fitness_goals",
					"Customer-gender",
					"Customer-trainer",
					"Customer-trainer-read_only",
					"Employee-certifications",
					"Employee-hourly_rate",
					"Employee-is_fitness_trainer",
					"Employee-is_fitness_trainer-default",
					"Employee-trainer_specialty"
				]
			]
		]
	}
]
