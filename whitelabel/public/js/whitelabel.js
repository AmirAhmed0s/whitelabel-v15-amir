$(window).on('load', function() {
    frappe.after_ajax(function () {
        var ws = frappe.boot.whitelabel_setting;
        if (!ws) return;

        if (ws.show_help_menu) {
            $('.dropdown-help').attr('style', 'display: block !important');
        }
        if (ws.logo_width) {
            $('.app-logo').css('width', ws.logo_width + 'px');
        }
        if (ws.logo_height) {
            $('.app-logo').css('height', ws.logo_height + 'px');
        }
        if (ws.navbar_background_color) {
            $('.navbar').css('background-color', ws.navbar_background_color);
        }
        if (ws.custom_navbar_title_style && ws.custom_navbar_title) {
            // Sanitize the style string – remove anything that could be an XSS vector
            var safeStyle = ws.custom_navbar_title_style.replace(/[<>'"{}\\]/g, '').replace(/\n/g, '');
            $('<span style="' + safeStyle + '" class="hidden-xs hidden-sm">'
                + frappe.utils.escape_html(ws.custom_navbar_title) + '</span>'
            ).insertAfter("#navbar-breadcrumbs");
        }
    });
});

// Manager Permission: filter the employee field on managed doctypes so that
// managers can only select employees assigned to them.
(function () {
    var MANAGED_DOCTYPES = [
        "Leave Application",
        "Loan Application",
        "Clearance Form",
        "Visit Form",
        "Permission Application"
    ];

    function apply_employee_filter(frm) {
        // manager_allowed_employees is set in boot_session only for managers.
        // Privileged users (System Manager, HR Manager, Administrator) and
        // users without a Manager Permissions record do not have this key set.
        var allowed = frappe.boot.manager_allowed_employees;
        if (allowed === undefined || allowed === null) {
            return;
        }

        frm.set_query("employee", function () {
            // Use a value that cannot match any real Employee name when the
            // manager has no assigned employees, so the drop-down is empty.
            var filter_list = allowed.length ? allowed : ["__no_employee__"];
            return { filters: { name: ["in", filter_list] } };
        });
    }

    MANAGED_DOCTYPES.forEach(function (doctype) {
        frappe.ui.form.on(doctype, {
            onload: function (frm) {
                apply_employee_filter(frm);
            }
        });
    });
}());
