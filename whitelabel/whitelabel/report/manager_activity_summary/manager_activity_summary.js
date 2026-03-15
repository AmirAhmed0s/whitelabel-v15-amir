// Copyright (c) 2024, Contributors and contributors
// For license information, please see license.txt

frappe.query_reports["Manager Activity Summary"] = {
	filters: [
		{
			fieldname: "manager",
			label: __("Manager"),
			fieldtype: "Link",
			options: "User",
			reqd: 1,
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

	onload: function (report) {
		// Delegated click handler for count-badge links.
		// Reads routing data from data-* attributes to avoid inline script injection.
		report.wrapper.on("click", ".mas-count-link", function (e) {
			e.preventDefault();
			const $el = $(this);
			const doctype    = $el.data("doctype");
			const employee   = $el.data("employee");
			const date_field = $el.data("date-field") || "posting_date";
			const from_date  = $el.data("from-date") || "";
			const to_date    = $el.data("to-date")   || "";
			const list_filters = { employee };
			if (from_date || to_date) {
				list_filters[date_field] = ["Between", [from_date, to_date]];
			}
			frappe.set_route("List", doctype, list_filters);
		});
	},

	formatter: function (value, row, column, data, default_formatter) {
		// Employee ID column – wrap in a styled badge
		if (column.fieldname === "employee") {
			const safe = frappe.utils.escape_html
				? frappe.utils.escape_html(value || "")
				: (value || "").replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
			return `<span class="mas-employee-badge">${safe}</span>`;
		}

		// Employee name column
		if (column.fieldname === "employee_name") {
			const safe = frappe.utils.escape_html
				? frappe.utils.escape_html(value || "")
				: (value || "").replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
			return `<span class="mas-employee-cell">${safe}</span>`;
		}

		// Numeric count columns – color-code and make clickable via data-* attributes
		if (
			column.fieldtype === "Int" &&
			column.fieldname !== "employee" &&
			column.fieldname !== "employee_name"
		) {
			const num = parseInt(value) || 0;
			let cls = "mas-count-zero";
			if (num >= 4) cls = "mas-count-high";
			else if (num >= 1) cls = "mas-count-low";

			const filters_val = frappe.query_report.get_filter_values();
			const from_date  = filters_val.from_date || "";
			const to_date    = filters_val.to_date   || "";
			const employee   = (data && data.employee) ? data.employee : "";
			const doctype    = column.label;
			// date_field is populated by the Python backend in the column definition
			const date_field = column.date_field || "posting_date";

			// All dynamic data stored in data-* attributes; click handled by delegated listener
			return (
				`<a href="#" class="mas-count-badge mas-count-link ${cls}" ` +
				`data-doctype="${frappe.utils.escape_html ? frappe.utils.escape_html(doctype) : doctype}" ` +
				`data-employee="${frappe.utils.escape_html ? frappe.utils.escape_html(employee) : employee}" ` +
				`data-date-field="${date_field}" ` +
				`data-from-date="${from_date}" ` +
				`data-to-date="${to_date}" ` +
				`title="${__("View {0} records for {1}", [doctype, employee])}">${num}</a>`
			);
		}

		return default_formatter(value, row, column, data);
	},
};
