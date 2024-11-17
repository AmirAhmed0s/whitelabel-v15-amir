# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from . import __logo__ as app_logo


app_name = "ksa_zatca"
app_title = "ksa_zatca"
app_publisher = "Bhavesh Maheshwari"
app_description = "ERPNext ksa_zatca"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "maheshwaribhavesh95863@gmail.com"
app_license = "MIT"
app_logo_url = '/assets/ksa_zatca/images/ksa_zatca_logo.jpg'

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/ksa_zatca/css/ksa_zatca_app.css"
app_include_js = "/assets/ksa_zatca/js/ksa_zatca.js"

# include js, css files in header of web template
web_include_css = "/assets/ksa_zatca/css/ksa_zatca_web.css"
# web_include_js = "/assets/ksa_zatca/js/ksa_zatca.js"

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

# Website user home page (by function)
# get_website_user_home_page = "ksa_zatca.utils.get_home_page"

website_context = {
	"favicon": app_logo or "/assets/ksa_zatca/images/ksa_zatca_logo.jpg",
	"splash_image": app_logo or "/assets/ksa_zatca/images/ksa_zatca_logo.jpg"
}
after_migrate = ['ksa_zatca.api.ksa_zatca_patch']

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ksa_zatca.install.before_install"
# after_install = "ksa_zatca.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ksa_zatca.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

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
# 		"ksa_zatca.tasks.all"
# 	],
# 	"daily": [
# 		"ksa_zatca.tasks.daily"
# 	],
# 	"hourly": [
# 		"ksa_zatca.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ksa_zatca.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ksa_zatca.tasks.monthly"
# 	]
# }

boot_session = "ksa_zatca.api.boot_session"
# Testing
# -------

# before_tests = "ksa_zatca.install.before_tests"

fixtures = [
    {"dt": "Custom Field", "filters": [["Translation","source_text","like","%ERPNext%"]]}
]

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ksa_zatca.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ksa_zatca.task.get_dashboard_data"
# }

# override_whitelisted_methods = {
# 	"frappe.utils.change_log.show_update_popup": "ksa_zatca.api.ignore_update_popup"
# }

