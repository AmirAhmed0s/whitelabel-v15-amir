from __future__ import unicode_literals
import frappe
import json
from frappe.utils import floor, flt, today, cint
from frappe import _

def whitelabel_patch():
	# delete erpnext welcome page
	frappe.delete_doc_if_exists('Page', 'welcome-to-erpnext', force=1)
	# update Welcome Blog Post
	if frappe.db.exists("Blog Post", "Welcome"):
		frappe.db.set_value("Blog Post", "Welcome", "content", "")
	update_field_label()
	if cint(get_frappe_version()) >= 13 and not frappe.db.get_single_value('Whitelabel Setting', 'ignore_onboard_whitelabel'):
		update_onboard_details()


def update_field_label():
	"""Update label of section break in employee doctype"""
	frappe.db.sql("""Update `tabDocField` set label='ERP' where fieldname='erpnext_user' and parent='Employee'""")

def get_frappe_version():
	return frappe.db.get_value("Installed Application", {"app_name": "frappe"}, "app_version").split('.')[0]

def update_onboard_details():
	update_onboard_module()
	update_onborad_steps()

def update_onboard_module():
	onboard_module_details = frappe.get_all("Module Onboarding", filters={}, fields=["name"])
	for row in onboard_module_details:
		doc = frappe.get_doc("Module Onboarding", row.name)
		doc.documentation_url = ""
		doc.flags.ignore_mandatory = True
		doc.save(ignore_permissions=True)

def update_onborad_steps():
	onboard_steps_details = frappe.get_all("Onboarding Step", filters={}, fields=["name"])
	for row in onboard_steps_details:
		doc = frappe.get_doc("Onboarding Step", row.name)
		doc.intro_video_url = ""
		doc.description = ""
		doc.flags.ignore_mandatory = True
		doc.save(ignore_permissions=True)

def boot_session(bootinfo):
	"""boot session - send whitelabel info if not guest"""
	if frappe.session['user'] != 'Guest':
		if frappe.db.exists("DocType", "Whitelabel Setting"):
			try:
				bootinfo.whitelabel_setting = frappe.get_doc("Whitelabel Setting", "Whitelabel Setting")
			except Exception:
				pass

		# Expose allowed employees for UI employee-field filtering on managed doctypes
		try:
			from whitelabel.whitelabel.manager_permission import (
				_user_bypasses,
				_get_manager_doc,
				get_allowed_employees,
			)
			user = frappe.session['user']
			if not _user_bypasses(user):
				mgr_doc = _get_manager_doc(user)
				if mgr_doc:
					bootinfo.manager_allowed_employees = get_allowed_employees(user)
		except Exception:
			pass


@frappe.whitelist()
def get_whitelabel_settings():
	"""Return whitelabel settings as a dict for frontend consumption."""
	if not frappe.db.exists("DocType", "Whitelabel Setting"):
		return {}
	try:
		doc = frappe.get_doc("Whitelabel Setting", "Whitelabel Setting")
		return {
			"app_name": doc.get("app_name") or "",
			"application_logo": doc.get("application_logo") or "",
			"navbar_background_color": doc.get("navbar_background_color") or "",
			"custom_navbar_title": doc.get("custom_navbar_title") or "",
			"custom_navbar_title_style": doc.get("custom_navbar_title_style") or "",
			"logo_height": doc.get("logo_height") or "",
			"logo_width": doc.get("logo_width") or "",
			"show_help_menu": cint(doc.get("show_help_menu")),
			"disable_new_update_popup": cint(doc.get("disable_new_update_popup")),
		}
	except Exception:
		return {}


@frappe.whitelist()
def ignore_update_popup():
	if not frappe.db.get_single_value('Whitelabel Setting', 'disable_new_update_popup'):
		show_update_popup_update()

@frappe.whitelist()
def show_update_popup_update():
	cache = frappe.cache()
	user = frappe.session.user
	update_info = cache.get_value("update-info")
	if not update_info:
		return

	updates = json.loads(update_info)

	update_message = ""
	if cache.sismember("update-user-set", user):
		for update_type in updates:
			release_links = ""
			for app in updates[update_type]:
				app = frappe._dict(app)
				release_links += "<b>{title}</b>: <a href='https://github.com/{org_name}/{app_name}/releases/tag/v{available_version}'>v{available_version}</a><br>".format(
					available_version=app.available_version,
					org_name=app.org_name,
					app_name=app.app_name,
					title=app.title
				)
			if release_links:
				message = _("New {} releases for the following apps are available").format(_(update_type))
				update_message += "<div class='new-version-log'>{0}<div class='new-version-links'>{1}</div></div>".format(message, release_links)

	if update_message:
		frappe.msgprint(update_message, title=_("New updates are available"), indicator='green')
		cache.srem("update-user-set", user)
