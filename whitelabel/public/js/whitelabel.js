$(window).on('load', function() {
    frappe.after_ajax(function () {
        if (frappe.boot.ksa_zatca_setting.show_help_menu) {
            // $('.dropdown-help').css('display','block');
            $('.dropdown-help').attr('style', 'display: block !important');
        }
        if (frappe.boot.ksa_zatca_setting.logo_width) {
            $('.app-logo').css('width',frappe.boot.ksa_zatca_setting.logo_width+'px');
        }
        if (frappe.boot.ksa_zatca_setting.logo_height) {
            $('.app-logo').css('height',frappe.boot.ksa_zatca_setting.logo_height+'px');
        }
        if (frappe.boot.ksa_zatca_setting.navbar_background_color) {
            $('.navbar').css('background-color',frappe.boot.ksa_zatca_setting.navbar_background_color)
        }
        if (frappe.boot.ksa_zatca_setting.custom_navbar_title_style && frappe.boot.ksa_zatca_setting.custom_navbar_title) {
            $(`<span style=${frappe.boot.ksa_zatca_setting.custom_navbar_title_style.replace('\n','')} class="hidden-xs hidden-sm">${frappe.boot.ksa_zatca_setting.custom_navbar_title}</span>`).insertAfter("#navbar-breadcrumbs")
        }
    })
})
