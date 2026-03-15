// Copyright (c) 2024, Contributors and contributors
// For license information, please see license.txt

frappe.ui.form.on('Whitelabel Setting', {
	refresh: function (frm) {
		frm.trigger('preview_logo');
		frm.trigger('add_preview_button');
	},

	after_save: function (frm) {
		frappe.ui.toolbar.clear_cache();
		frappe.show_alert({ message: __('Whitelabel settings applied. Refresh the page to see changes.'), indicator: 'green' });
	},

	application_logo: function (frm) {
		frm.trigger('preview_logo');
	},

	preview_logo: function (frm) {
		const logo = frm.doc.application_logo;
		if (logo) {
			frm.set_intro(
				`<div style="padding:8px 0">
					<strong>${__('Logo Preview')}:</strong><br>
					<img src="${logo}" style="max-height:80px;max-width:300px;margin-top:6px;border:1px solid #ddd;padding:4px;border-radius:4px" />
				</div>`,
				'blue'
			);
		} else {
			frm.set_intro('');
		}
	},

	add_preview_button: function (frm) {
		frm.add_custom_button(__('Preview Navbar Color'), function () {
			const color = frm.doc.navbar_background_color;
			if (!color) {
				frappe.msgprint(__('Please enter a Navbar Background Color first.'));
				return;
			}
			// Only allow hex colors in the style attribute to prevent injection
			if (!/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/.test(color)) {
				frappe.msgprint(__('Please enter a valid hex color (e.g. #1F3B4D).'));
				return;
			}
			frappe.show_alert({
				message: `<span style="background:${color};color:#fff;padding:4px 12px;border-radius:4px">${__('Navbar Color Preview')}</span>`,
				indicator: 'blue'
			}, 5);
		}, __('Actions'));

		frm.add_custom_button(__('Reset to Defaults'), function () {
			frappe.confirm(__('Reset all Whitelabel settings to defaults?'), function () {
				frm.set_value('application_logo', '');
				frm.set_value('navbar_background_color', '');
				frm.set_value('custom_navbar_title', '');
				frm.set_value('custom_navbar_title_style', '');
				frm.set_value('app_name', '');
				frm.set_value('logo_height', '');
				frm.set_value('logo_width', '');
				frm.set_value('disable_new_update_popup', 0);
				frm.set_value('ignore_onboard_whitelabel', 0);
				frm.set_value('show_help_menu', 0);
				frm.set_value('disable_standard_footer', 0);
				frm.set_value('email_footer_address', '');
				frm.save().then(() => {
					frappe.show_alert({ message: __('Settings reset to defaults.'), indicator: 'orange' });
				});
			});
		}, __('Actions'));
	},

	navbar_background_color: function (frm) {
		// Live preview of the color in the field row itself
		const color = frm.doc.navbar_background_color;
		if (color && /^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/.test(color)) {
			$(frm.fields_dict.navbar_background_color.wrapper).css('border-left', `4px solid ${color}`);
		} else {
			$(frm.fields_dict.navbar_background_color.wrapper).css('border-left', '');
		}
	},
});
