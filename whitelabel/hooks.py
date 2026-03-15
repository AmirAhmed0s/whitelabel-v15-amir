# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "whitelabel"
app_title = "Whitelabel"
app_publisher = "Amir Ahmed"
app_description = "Whitelabel app for Frappe/ERPNext v15 — custom branding, logo, navbar and manager-permission controls"
app_icon = "octicon octicon-paintcan"
app_color = "blue"
app_email = ""
app_license = "MIT"
app_logo_url = '/assets/whitelabel/images/whitelabel_logo.jpg'

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/whitelabel/css/whitelabel_app.css"
app_include_js = "/assets/whitelabel/js/whitelabel.js"

# include js, css files in header of web template
web_include_css = "/assets/whitelabel/css/whitelabel_web.css"
# web_include_js = "/assets/whitelabel/js/whitelabel.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

website_context = {
	"favicon": "/assets/whitelabel/images/whitelabel_logo.jpg",
	"splash_image": "/assets/whitelabel/images/whitelabel_logo.jpg"
}

after_migrate = ['whitelabel.api.whitelabel_patch']

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "whitelabel.install.before_install"
# after_install = "whitelabel.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "whitelabel.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways
#
# Manager Permissions: restrict manager users to their assigned employees and
# DocTypes as configured in the "Manager Permissions" DocType.

_MANAGER_PERM_MODULE = "whitelabel.whitelabel.manager_permission"

permission_query_conditions = {
	"Leave Application":    _MANAGER_PERM_MODULE + ".get_permission_query_conditions",
	"Loan Application":     _MANAGER_PERM_MODULE + ".get_permission_query_conditions",
	"Clearance Form":       _MANAGER_PERM_MODULE + ".get_permission_query_conditions",
	"Visit Form":           _MANAGER_PERM_MODULE + ".get_permission_query_conditions",
	"Permission Application": _MANAGER_PERM_MODULE + ".get_permission_query_conditions",
}

has_permission = {
	"Leave Application":    _MANAGER_PERM_MODULE + ".has_permission",
	"Loan Application":     _MANAGER_PERM_MODULE + ".has_permission",
	"Clearance Form":       _MANAGER_PERM_MODULE + ".has_permission",
	"Visit Form":           _MANAGER_PERM_MODULE + ".has_permission",
	"Permission Application": _MANAGER_PERM_MODULE + ".has_permission",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"whitelabel.tasks.all"
# 	],
# 	"daily": [
# 		"whitelabel.tasks.daily"
# 	],
# 	"hourly": [
# 		"whitelabel.tasks.hourly"
# 	],
# 	"weekly": [
# 		"whitelabel.tasks.weekly"
# 	]
# 	"monthly": [
# 		"whitelabel.tasks.monthly"
# 	]
# }

boot_session = "whitelabel.api.boot_session"

# Testing
# -------

# before_tests = "whitelabel.install.before_tests"

fixtures = [
    {"dt": "Custom Field", "filters": [["Translation","source_text","like","%ERPNext%"]]}
]

# Overriding Methods
# ------------------------------

# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "whitelabel.event.get_events"
# }

# override_doctype_dashboards = {
# 	"Task": "whitelabel.task.get_dashboard_data"
# }

