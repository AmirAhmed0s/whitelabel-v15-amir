# -*- coding: utf-8 -*-
# Copyright (c) 2021, Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import re
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.installer import update_site_config


class WhitelabelSetting(Document):
	def validate(self):
		self._validate_hex_color()
		system_settings_doc = frappe.get_doc("System Settings", "System Settings")
		navbar_settings_doc = frappe.get_doc("Navbar Settings", "Navbar Settings")
		website_doc = frappe.get_doc("Website Settings", "Website Settings")
		self.set_app_name(system_settings_doc)
		self.set_theme_attr(navbar_settings_doc, website_doc)
		self.disable_onboarding(system_settings_doc)
		self.set_log_notification(system_settings_doc)
		self.set_footer(system_settings_doc)
		system_settings_doc.save(ignore_permissions=True)
		navbar_settings_doc.save(ignore_permissions=True)
		website_doc.save(ignore_permissions=True)

	def _validate_hex_color(self):
		"""Validate hex color codes in navbar_background_color."""
		color = (self.navbar_background_color or "").strip()
		if color and not re.match(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$', color):
			frappe.throw(
				_("Navbar Background Color must be a valid hex color code (e.g. #1F3B4D or #FFF)"),
				frappe.ValidationError,
			)

	def set_app_name(self, system_settings_doc):
		if self.app_name:
			system_settings_doc.app_name = self.app_name
		else:
			if "erpnext" in frappe.get_installed_apps():
				system_settings_doc.app_name = "ERPNext"
			else:
				system_settings_doc.app_name = "Frappe"

	def set_theme_attr(self, navbar_settings_doc, website_doc):
		if self.application_logo:
			navbar_settings_doc.app_logo = self.application_logo
			website_doc.app_logo = self.application_logo
			website_doc.splash_image = self.application_logo
			update_site_config("app_logo_url", self.application_logo)
			frappe.clear_cache()
		else:
			navbar_settings_doc.app_logo = ""
			website_doc.app_logo = ""
			website_doc.splash_image = ""
			update_site_config("app_logo_url", False)
			frappe.clear_cache()

		if self.navbar_background_color:
			navbar_settings_doc.brand_html = self._build_navbar_brand_html()
		else:
			navbar_settings_doc.brand_html = ""

	def _build_navbar_brand_html(self):
		"""Build a CSS snippet to apply the custom navbar color."""
		color = self.navbar_background_color or ""
		if not color:
			return ""
		title = frappe.utils.escape_html(self.custom_navbar_title or "")
		# Allow only safe CSS properties (strip dangerous characters like < > { })
		style_extra = re.sub(r'[<>{}\'"\\]', '', self.custom_navbar_title_style or "")
		html = ""
		if title:
			html = "<span style='color:{color};{style}'>{title}</span>".format(
				color=frappe.utils.escape_html(color),
				style=style_extra,
				title=title,
			)
		return html

	def disable_onboarding(self, system_settings_doc):
		if self.ignore_onboard_whitelabel == 1:
			system_settings_doc.enable_onboarding = 0
		else:
			system_settings_doc.enable_onboarding = 1

	def set_log_notification(self, system_settings_doc):
		system_settings_doc.disable_system_update_notification = self.disable_new_update_popup
		system_settings_doc.disable_change_log_notification = self.disable_new_update_popup

	def set_footer(self, system_settings_doc):
		system_settings_doc.email_footer_address = self.email_footer_address
		system_settings_doc.disable_standard_email_footer = self.disable_standard_footer
		system_settings_doc.hide_footer_in_auto_email_reports = self.disable_standard_footer

