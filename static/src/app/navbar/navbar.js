/** @odoo-module **/

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";

// Patch the Navbar component to use the correct company logo
patch(Navbar.prototype, {
    setup() {
        super.setup(...arguments);
    },
    
    get logoUrl() {
        // Get company ID from POS
        const company = this.pos?.company;
        if (company && company.id) {
            // Return the company logo URL
            return `/web/image/res.company/${company.id}/logo?unique=${Date.now()}`;
        }
        // Fallback to default logo
        return '/web/static/img/logo.png';
    }
});
