# -*- coding: utf-8 -*-
# Copyright (c) 2024, Contributors and contributors
# For license information, please see license.txt
#
# Manager Permission Logic
# ========================
# This module provides Frappe permission hooks that enforce manager-level access
# control based on the "Manager Permissions" DocType.
#
# How it works:
#   1. When a manager (non-System-Manager / non-HR-Manager) tries to access a
#      list view of a managed DocType, `get_permission_query_conditions` appends
#      a WHERE clause that limits rows to employees assigned to that manager.
#   2. When a manager opens a specific document, `has_permission` verifies that
#      the record belongs to one of their allowed employees AND that the requested
#      permission type (read / write) is allowed.
#   3. Users with "System Manager" or "HR Manager" roles bypass all extra checks.

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint

# Name of the field that stores the employee reference on HR transaction DocTypes
EMPLOYEE_FIELD = "employee"

# Privileged roles that are never restricted by Manager Permissions
BYPASS_ROLES = {"System Manager", "HR Manager", "Administrator"}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _user_bypasses(user):
	"""Return True if the user has a privileged role that skips manager checks."""
	if user == "Administrator":
		return True
	roles = set(frappe.get_roles(user))
	return bool(roles & BYPASS_ROLES)


def _get_manager_doc(user):
	"""Return the Manager Permissions document for *user*, or None."""
	name = frappe.db.get_value("Manager Permissions", {"manager": user}, "name")
	if not name:
		return None
	return frappe.get_cached_doc("Manager Permissions", name)


def get_allowed_employees(user=None):
	"""Return list of employee IDs that *user* is allowed to see."""
	if not user:
		user = frappe.session.user
	mgr_doc = _get_manager_doc(user)
	if not mgr_doc:
		return []
	return [row.employee for row in (mgr_doc.employees or []) if row.employee]


def get_allowed_doctypes(user=None):
	"""Return a dict: {doctype: {"read_only": bool, "edit_access": bool}}."""
	if not user:
		user = frappe.session.user
	mgr_doc = _get_manager_doc(user)
	if not mgr_doc:
		return {}
	result = {}
	for row in (mgr_doc.accessible_documents or []):
		if row.document_type:
			result[row.document_type] = {
				"read_only": cint(row.read_only),
				"edit_access": cint(row.edit_access),
			}
	return result


# ---------------------------------------------------------------------------
# Frappe permission hooks
# ---------------------------------------------------------------------------

def get_permission_query_conditions(user, doctype=None):
	"""
	Hook: permission_query_conditions
	Appends a SQL WHERE clause so list views only show records belonging to
	employees managed by *user*.
	Called by Frappe as: get_permission_query_conditions(user)
	The doctype is resolved through the hook key, not a parameter.
	"""
	if not user:
		user = frappe.session.user

	# Privileged users see everything
	if _user_bypasses(user):
		return ""

	# If no Manager Permissions record exists, this hook does nothing (let
	# standard Frappe permissions handle the request)
	mgr_doc = _get_manager_doc(user)
	if not mgr_doc:
		return ""

	allowed_employees = get_allowed_employees(user)
	if not allowed_employees:
		# Manager exists but has no employees → deny all
		return "1=0"

	# Build a safe IN list using frappe.db.escape
	escaped = ", ".join(frappe.db.escape(e) for e in allowed_employees)

	# We do not know the doctype here (hook is keyed per-doctype in hooks.py),
	# so we use a generic reference.  Frappe passes the correct table context.
	return "`{table}`.`{field}` IN ({employees})".format(
		table="tab" + (doctype or ""),
		field=EMPLOYEE_FIELD,
		employees=escaped,
	)


def has_permission(doc, ptype="read", user=None):
	"""
	Hook: has_permission
	Called per-document to verify access.
	Returns:
	  True  – access granted
	  False – access denied
	  None  – defer to standard Frappe permission system
	"""
	if not user:
		user = frappe.session.user

	# Privileged roles pass through
	if _user_bypasses(user):
		return None

	# No Manager Permissions → nothing to enforce here
	mgr_doc = _get_manager_doc(user)
	if not mgr_doc:
		return None

	allowed_doctypes = get_allowed_doctypes(user)
	doc_type = doc.doctype

	if doc_type not in allowed_doctypes:
		return False

	# Check the employee field on the document
	allowed_employees = get_allowed_employees(user)
	doc_employee = doc.get(EMPLOYEE_FIELD)
	if doc_employee and doc_employee not in allowed_employees:
		return False

	# Enforce read-only vs edit-access
	doctype_cfg = allowed_doctypes[doc_type]
	write_operations = {"write", "submit", "cancel", "amend", "delete"}
	if ptype in write_operations:
		if not doctype_cfg.get("edit_access"):
			frappe.throw(
				_("You only have Read Only access to {0} documents.").format(_(doc_type)),
				frappe.PermissionError,
			)
			return False

	return True
