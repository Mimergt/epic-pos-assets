# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import base64
import os
import logging

_logger = logging.getLogger(__name__)


class PosAssetManager(models.Model):
    _name = 'epic.asset'
    _description = 'Epic Asset Manager'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    asset_type = fields.Selection([
        ('logo_main', 'Logo Main'),
        ('logo_dark', 'Logo Dark'),
        ('logo_light', 'Logo Light'),
        ('logo_pos', 'Logo POS Header'),
        ('favicon', 'Favicon'),
        ('splash', 'Splash Screen'),
        ('logo_ticket', 'Logo Ticket/Receipt'),
        ('watermark', 'Watermark'),
        ('signature', 'Signature'),
        ('placeholder', 'Product Placeholder'),
        ('category_image', 'Category Image'),
        ('product_image', 'Product Image'),
        ('button_icon', 'Button Icon'),
        ('background', 'Background'),
        ('modal_bg', 'Modal Background'),
        ('logo_client', 'Customer Display Logo'),
        ('banner', 'Banner'),
        ('customer_bg', 'Customer Display Background'),
        ('other', 'Other')
    ], string='Asset Type', required=True, default='other')
    asset_category = fields.Selection([
        ('logos', 'Logos'),
        ('receipts', 'Receipts'),
        ('products', 'Products'),
        ('ui', 'UI Elements'),
        ('customer_display', 'Customer Display'),
        ('other', 'Other')
    ], string='Category', compute='_compute_category', store=True)
    file_data = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')
    file_path = fields.Char('Target File Path', compute='_compute_file_path', store=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    applied = fields.Boolean('Applied to System', default=False)
    applied_date = fields.Datetime('Last Applied Date')

    @api.depends('asset_type')
    def _compute_category(self):
        """Compute category based on asset type"""
        category_map = {
            'logo_main': 'logos',
            'logo_dark': 'logos',
            'logo_light': 'logos',
            'logo_pos': 'logos',
            'favicon': 'logos',
            'splash': 'logos',
            'logo_ticket': 'receipts',
            'watermark': 'receipts',
            'signature': 'receipts',
            'placeholder': 'products',
            'category_image': 'products',
            'product_image': 'products',
            'button_icon': 'ui',
            'background': 'ui',
            'modal_bg': 'ui',
            'logo_client': 'customer_display',
            'banner': 'customer_display',
            'customer_bg': 'customer_display',
        }
        for record in self:
            record.asset_category = category_map.get(record.asset_type, 'other')

    @api.depends('asset_type', 'file_name')
    def _compute_file_path(self):
        """Compute the target file path based on asset type"""
        path_map = {
            'logo_main': 'logos/logo_main.png',
            'logo_dark': 'logos/logo_dark.png',
            'logo_light': 'logos/logo_light.png',
            'logo_pos': 'logos/logo_pos.png',
            'favicon': 'logos/favicon.png',
            'splash': 'logos/splash.jpg',
            'logo_ticket': 'receipts/logo_ticket.png',
            'watermark': 'receipts/watermark.png',
            'signature': 'receipts/signature.png',
            'placeholder': 'products/placeholder.png',
            'background': 'ui/background.jpg',
            'modal_bg': 'ui/modal_bg.png',
            'logo_client': 'customer_display/logo_client.png',
            'banner': 'customer_display/banner.jpg',
            'customer_bg': 'customer_display/background.jpg',
        }
        for record in self:
            if record.asset_type in path_map:
                record.file_path = path_map[record.asset_type]
            elif record.file_name:
                # For dynamic types like category_* or product_*
                category_folder = record.asset_category or 'other'
                record.file_path = f"{category_folder}/{record.file_name}"
            else:
                record.file_path = False

    def action_apply_asset(self):
        """Apply the asset to the system"""
        self.ensure_one()
        
        try:
            company = self.env.company
            
            if self.asset_type == 'favicon':
                # In Odoo 18, favicon is stored in logo_web field
                company.write({
                    'logo_web': self.file_data
                })
                _logger.info(f"Favicon applied to company {company.name} using logo_web field")
                
            elif self.asset_type in ['logo_main', 'logo_dark', 'logo_light']:
                # Apply logo to Odoo company
                company.write({
                    'logo': self.file_data
                })
                _logger.info(f"Logo applied to company {company.name}")
                
            elif self.asset_type == 'logo_pos':
                # Apply logo to POS - store in company logo field which POS uses
                company.write({
                    'logo': self.file_data
                })
                _logger.info(f"POS Header Logo applied to company {company.name}")
                
                # Clear caches to force reload
                try:
                    # Clear Qweb cache if available
                    if hasattr(self.env['ir.qweb'], '_clear_cache'):
                        self.env['ir.qweb']._clear_cache()
                        _logger.info("Cleared Qweb cache")
                except Exception as e:
                    _logger.warning(f"Could not clear Qweb cache: {str(e)}")
                
                try:
                    # Clear registry cache
                    self.env.registry.clear_cache()
                    _logger.info("Cleared registry cache")
                except Exception as e:
                    _logger.warning(f"Could not clear registry cache: {str(e)}")
                
            elif self.asset_type == 'logo_ticket':
                # Apply receipt logo
                # This will be stored in the asset for POS to use
                _logger.info(f"Receipt logo ready for POS: {self.name}")
                
            else:
                # For other asset types, store in filestore or make available to POS
                _logger.info(f"Asset {self.name} stored and ready for use")
            
            # Mark as applied
            self.write({
                'applied': True,
                'applied_date': fields.Datetime.now()
            })
            
            # Special message for POS logo
            if self.asset_type == 'logo_pos':
                message = _('POS logo has been applied to the company successfully.\n\nIMPORTANT STEPS:\n1. The logo is saved at: /web/image/res.company/%s/logo\n2. Close ALL open POS sessions\n3. Clear browser cache: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)\n4. Or use Incognito/Private mode\n5. Open a new POS session\n\nNote: The POS uses the company logo. If it doesn\'t appear, verify the logo is visible at the URL above.') % company.id
            else:
                message = _('Asset "%s" has been applied successfully. Refresh your browser (Ctrl+Shift+R) to see changes.') % self.name
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"Error applying asset {self.name}: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Error'),
                    'message': _('Failed to apply asset: %s') % str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }

    @api.model
    def update_pos_assets(self, assets_data):
        """Update POS assets from uploaded data"""
        for asset in assets_data:
            existing = self.search([
                ('name', '=', asset['name']),
                ('asset_type', '=', asset['type'])
            ], limit=1)
            
            vals = {
                'name': asset['name'],
                'asset_type': asset['type'],
                'file_data': asset['data'],
                'file_name': asset['filename'],
                'description': asset.get('description', '')
            }
            
            if existing:
                existing.write(vals)
                _logger.info(f"Updated asset: {asset['name']}")
            else:
                self.create(vals)
                _logger.info(f"Created new asset: {asset['name']}")
        
        return True