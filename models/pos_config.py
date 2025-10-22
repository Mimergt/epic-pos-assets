# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _get_logo_url(self):
        """Override to ensure POS gets the correct company logo"""
        self.ensure_one()
        if self.company_id.logo:
            return f'/web/image/res.company/{self.company_id.id}/logo'
        return '/web/static/img/logo.png'

    @api.model
    def load_logo_for_pos(self):
        """Load the company logo for POS display"""
        company = self.env.company
        if company.logo:
            return {
                'logo_url': f'/web/image/res.company/{company.id}/logo',
                'has_custom_logo': True
            }
        return {
            'logo_url': '/web/static/img/logo.png',
            'has_custom_logo': False
        }
