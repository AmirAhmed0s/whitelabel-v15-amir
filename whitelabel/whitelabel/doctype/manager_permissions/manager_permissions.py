# -*- coding: utf-8 -*-
# Copyright (c) 2024, Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

# Default DocTypes to pre-populate in every new Manager Permissions record
DEFAULT_ACCESSIBLE_DOCTYPES = [
	{"document_type": "Loan Application", "read_only": 1, "edit_access": 1},
	{"document_type": "Leave Application", "read_only": 1, "edit_access": 1},
	{"document_type": "Clearance Form", "read_only": 1, "edit_access": 1},
	{"document_type": "Visit Form", "read_only": 1, "edit_access": 1},
	{"document_type": "Permission Application", "read_only": 1, "edit_access": 1},
]


class ManagerPermissions(Document):
	def validate(self):
		self._validate_no_duplicate_employees()
		self._validate_no_duplicate_doctypes()

	def on_submit(self):
		pass

	def before_insert(self):
		"""Pre-populate accessible_documents with defaults when creating a new record."""
		if not self.accessible_documents:
			for row in DEFAULT_ACCESSIBLE_DOCTYPES:
				self.append("accessible_documents", row)

	# ------------------------------------------------------------------
	# Helpers
	# ------------------------------------------------------------------

	def _validate_no_duplicate_employees(self):
		seen = set()
		for row in self.employees or []:
			if row.employee in seen:
				frappe.throw(
					frappe._("Employee {0} is listed more than once in the Managed Employees table.").format(
						frappe.bold(row.employee)
					)
				)
			seen.add(row.employee)

	def _validate_no_duplicate_doctypes(self):
		seen = set()
		for row in self.accessible_documents or []:
			if row.document_type in seen:
				frappe.throw(
					frappe._("DocType {0} is listed more than once in the Accessible Documents table.").format(
						frappe.bold(row.document_type)
					)
				)
			seen.add(row.document_type)
