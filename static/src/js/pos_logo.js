/** @odoo-module **/

// Simple script to replace logo URL in POS
(function() {
    'use strict';
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        // Function to update logo
        function updatePosLogo() {
            const logoImages = document.querySelectorAll('img.pos-logo');
            logoImages.forEach(function(img) {
                if (img.src.includes('/web/static/img/logo.png')) {
                    // Get company ID from Odoo session
                    const companyId = odoo.session_info.company_id || 1;
                    const newSrc = `/web/image/res.company/${companyId}/logo?t=${Date.now()}`;
                    console.log('Updating POS logo from', img.src, 'to', newSrc);
                    img.src = newSrc;
                }
            });
        }
        
        // Update immediately
        updatePosLogo();
        
        // Also update periodically in case DOM changes
        setInterval(updatePosLogo, 1000);
        
        // Use MutationObserver to catch dynamically added logos
        const observer = new MutationObserver(function(mutations) {
            updatePosLogo();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
})();
