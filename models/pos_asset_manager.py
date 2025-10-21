# -*- coding: utf-8 -*-
from odoo import models, fields, api
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
        ('logo', 'Logo'),
        ('background', 'Background Image'),
        ('favicon', 'Favicon'),
        ('other', 'Other')
    ], string='Asset Type', required=True, default='logo')
    file_data = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')

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