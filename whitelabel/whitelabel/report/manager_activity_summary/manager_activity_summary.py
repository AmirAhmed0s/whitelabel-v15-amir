# -*- coding: utf-8 -*-
# Copyright (c) 2024, Contributors and contributors
# For license information, please see license.txt
#
# Script Report: Manager Activity Summary
# ========================================
# Shows transaction counts per employee/DocType for a given manager,
# based on the configuration in the Manager Permissions DocType.

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	validate_filters(filters)

	columns, data, summary = [], [], []

	# Resolve manager ─ use the current user when not System/HR Manager
	manager = get_effective_manager(filters)
	if not manager:
		frappe.throw(_("No Manager selected and current user has no Manager Permissions record."))

	# Fetch configuration from Manager Permissions
	mgr_config = get_manager_config(manager)
	if not mgr_config:
		frappe.msgprint(_("No Manager Permissions record found for {0}.").format(manager))
		return [], [], None

	employees = mgr_config["employees"]
	doctypes  = mgr_config["doctypes"]

	if not employees:
		frappe.msgprint(_("No employees configured for manager {0}.").format(manager))
		return [], [], None

	if not doctypes:
		frappe.msgprint(_("No accessible DocTypes configured for manager {0}.").format(manager))
		return [], [], None

	# Apply optional employee filter
	if filters.get("employee"):
		if filters.employee not in employees:
			frappe.throw(_("Employee {0} is not managed by {1}.").format(filters.employee, manager))
		employees = [filters.employee]

	# Build dynamic columns
	columns = build_columns(doctypes)

	# Build data rows
	data, total_transactions = build_data(employees, doctypes, filters)

	# Summary row
	summary = [
		{"value": len(employees), "label": _("Employees"), "datatype": "Int", "indicator": "blue"},
		{"value": total_transactions, "label": _("Transactions in Period"), "datatype": "Int", "indicator": "green"},
	]

	return columns, data, None, None, summary


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def validate_filters(filters):
	if filters.get("from_date") and filters.get("to_date"):
		if getdate(filters.from_date) > getdate(filters.to_date):
			frappe.throw(_("From Date cannot be greater than To Date."))


def get_effective_manager(filters):
	"""Return the manager to use for this report execution."""
	if filters.get("manager"):
		return filters.manager

	# Fall back to current user if they have a Manager Permissions record
	user = frappe.session.user
	if frappe.db.exists("Manager Permissions", {"manager": user}):
		return user
	return None


def get_manager_config(manager):
	"""
	Return:
	  {"employees": [emp_id, ...], "doctypes": [dt_name, ...]}
	or None if no record found.
	"""
	name = frappe.db.get_value("Manager Permissions", {"manager": manager}, "name")
	if not name:
		return None

	doc = frappe.get_doc("Manager Permissions", name)

	employees = [row.employee for row in (doc.employees or []) if row.employee]
	doctypes  = [row.document_type for row in (doc.accessible_documents or []) if row.document_type]

	return {"employees": employees, "doctypes": doctypes}


def build_columns(doctypes):
	"""Build report column definitions."""
	columns = [
		{
			"fieldname": "employee",
			"label": _("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 180,
		},
		{
			"fieldname": "employee_name",
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"width": 200,
		},
	]
	for dt in doctypes:
		columns.append(
			{
				"fieldname": frappe.scrub(dt),
				"label": _(dt),
				"fieldtype": "Int",
				"width": 160,
			}
		)
	return columns


def build_data(employees, doctypes, filters):
	"""
	Query transaction counts for each (employee, doctype) combination.
	Returns (rows, total_count).
	"""
	from_date = filters.get("from_date")
	to_date   = filters.get("to_date") or nowdate()

	# Fetch all counts in one query per doctype then pivot in Python
	# This avoids N×M queries.
	counts = {}  # {employee: {doctype: count}}
	for emp in employees:
		counts[emp] = {frappe.scrub(dt): 0 for dt in doctypes}

	total_transactions = 0

	for dt in doctypes:
		field_key = frappe.scrub(dt)
		try:
			result = get_doctype_counts(dt, employees, from_date, to_date)
		except Exception:
			# DocType may not exist yet or has no employee field – skip silently
			continue

		for emp, cnt in result.items():
			if emp in counts:
				counts[emp][field_key] = cnt
				total_transactions += cnt

	# Build final rows (sorted by employee for consistency)
	data = []
	for emp in sorted(employees):
		emp_name = frappe.db.get_value("Employee", emp, "employee_name") or emp
		row = {"employee": emp, "employee_name": emp_name}
		row.update(counts.get(emp, {}))
		data.append(row)

	return data, total_transactions


def get_doctype_counts(doctype, employees, from_date=None, to_date=None):
	"""
	Return {employee: count} for *doctype* within the given date range.
	Uses a single aggregated SQL query for performance.
	"""
	if not frappe.db.table_exists("tab" + doctype):
		return {}

	# Check if the doctype has a 'employee' field (creation is always present in Frappe)
	meta = frappe.get_meta(doctype)
	has_employee = meta.has_field("employee")

	if not has_employee:
		return {}

	conditions = []
	values = {"employees": employees}

	if from_date:
		conditions.append("DATE(`creation`) >= %(from_date)s")
		values["from_date"] = from_date
	if to_date:
		conditions.append("DATE(`creation`) <= %(to_date)s")
		values["to_date"] = to_date

	where_clause = ""
	if conditions:
		where_clause = "AND " + " AND ".join(conditions)

	sql = """
		SELECT
			`employee`,
			COUNT(`name`) AS `cnt`
		FROM
			`tab{doctype}`
		WHERE
			`employee` IN %(employees)s
			{where_clause}
		GROUP BY
			`employee`
	""".format(
		doctype=doctype,
		where_clause=where_clause,
	)

	rows = frappe.db.sql(sql, values, as_dict=True)
	return {r.employee: r.cnt for r in rows}
