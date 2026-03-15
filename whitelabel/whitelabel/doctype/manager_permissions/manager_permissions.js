// Copyright (c) 2024, Contributors and contributors
// For license information, please see license.txt

frappe.ui.form.on("Manager Permissions", {
	refresh: function (frm) {
		frm.trigger("apply_ui_enhancements");
	},

	apply_ui_enhancements: function (frm) {
		// Highlight the manager header section
		if (frm.fields_dict.manager) {
			$(frm.fields_dict.manager.wrapper).addClass("manager-permission-header");
		}

		// Badge-style highlights for the accessible documents grid
		frm.trigger("render_access_badges");
	},

	render_access_badges: function (frm) {
		if (!frm.fields_dict.accessible_documents) return;

		const grid = frm.fields_dict.accessible_documents.grid;
		if (!grid || !grid.data) return;

		grid.data.forEach(function (row, idx) {
			const $row = grid.grid_rows[idx];
			if (!$row) return;

			const has_edit = cint(row.edit_access);
			const has_read = cint(row.read_only);

			const badge_html = has_edit
				? `<span class="permission-badge permission-badge-edit">${__("Edit Access")}</span>`
				: has_read
				? `<span class="permission-badge permission-badge-read">${__("Read Only")}</span>`
				: "";

			const $badge_cell = $row.row.find(".col[data-fieldname='document_type']");
			$badge_cell.find(".permission-badge").remove();
			if (badge_html) {
				$badge_cell.append(badge_html);
			}
		});
	},

	accessible_documents_on_form_rendered: function (frm) {
		frm.trigger("render_access_badges");
	},
});

// Re-render badges when the child table rows change
frappe.ui.form.on("Manager Accessible Documents", {
	edit_access: function (frm) {
		frm.trigger("render_access_badges");
	},
	read_only: function (frm) {
		frm.trigger("render_access_badges");
	},
});
