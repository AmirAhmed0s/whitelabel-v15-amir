// Copyright (c) 2024, Contributors and contributors
// For license information, please see license.txt

frappe.query_reports["Manager Activity Summary"] = {
	filters: [
		{
			fieldname: "manager",
			label: __("Manager"),
			fieldtype: "Link",
			options: "User",
			reqd: 0,
			default: frappe.session.user,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			reqd: 0,
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		// Employee column – wrap in a styled badge
		if (column.fieldname === "employee") {
			return `<span class="employee-badge">${value || ""}</span>`;
		}

		if (column.fieldname === "employee_name") {
			return `<span class="employee-cell">${value || ""}</span>`;
		}

		// Numeric count columns – color-code based on value
		if (typeof value === "number" || (value !== null && value !== undefined && !isNaN(parseInt(value)))) {
			const num = parseInt(value) || 0;
			let cls = "count-zero";
			if (num >= 4) cls = "count-high";
			else if (num >= 1) cls = "count-low";

			const filters = frappe.query_report.get_filter_values();
			const from_date = filters.from_date || "";
			const to_date   = filters.to_date   || "";
			const employee  = data && data.employee ? data.employee : "";
			const doctype   = column.label;

			// Make count clickable → open the filtered list view
			const href = `/app/${frappe.router.slug(doctype)}?employee=${encodeURIComponent(employee)}&from_date=${from_date}&to_date=${to_date}`;
			return `<a href="${href}" class="count-badge ${cls}" title="${__('View {0} records for {1}', [doctype, employee])}">${num}</a>`;
		}

		return default_formatter(value, row, column, data);
	},
};
