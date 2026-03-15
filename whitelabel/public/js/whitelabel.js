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
