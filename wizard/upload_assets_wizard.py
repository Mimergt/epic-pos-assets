# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import zipfile
import io
import os
import mimetypes
import logging

_logger = logging.getLogger(__name__)


class UploadAssetsWizard(models.TransientModel):
    _name = 'epic.wizard'
    _description = 'Upload Assets Wizard'

    zip_file = fields.Binary('ZIP File', required=True, help="Upload a ZIP file containing logos and images")
    zip_filename = fields.Char('File Name')
    asset_type = fields.Selection([
        ('logo', 'Logo Files'),
        ('background', 'Background Images'),
        ('all', 'All Assets')
    ], string='Asset Type', required=True, default='all')
    
    @api.constrains('zip_file')
    def _check_zip_file(self):
        if self.zip_file:
            try:
                zip_data = base64.b64decode(self.zip_file)
                zipfile.ZipFile(io.BytesIO(zip_data))
            except Exception as e:
                raise ValidationError(_('Invalid ZIP file: %s') % str(e))

    def action_upload_assets(self):
        """Process the uploaded ZIP file and extract assets"""
        if not self.zip_file:
            raise UserError(_('Please select a ZIP file to upload.'))
        
        try:
            # Decode and open ZIP file
            zip_data = base64.b64decode(self.zip_file)
            zip_buffer = io.BytesIO(zip_data)
            
            assets_data = []
            allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp']
            
            with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                for file_info in zip_file.infolist():
                    # Skip directories and system files
                    if file_info.is_dir() or file_info.filename.startswith('__MACOSX/'):
                        continue
                    
                    file_ext = os.path.splitext(file_info.filename)[1].lower()
                    if file_ext not in allowed_extensions:
                        _logger.warning(f"Skipping unsupported file: {file_info.filename}")
                        continue
                    
                    # Extract file content
                    file_content = zip_file.read(file_info.filename)
                    file_b64 = base64.b64encode(file_content).decode('utf-8')
                    
                    # Determine asset type based on filename and path
                    filename_lower = file_info.filename.lower()
                    file_base = os.path.splitext(os.path.basename(file_info.filename))[0].lower()
                    
                    # Map based on your structure
                    if 'logo_main' in filename_lower or file_base == 'logo_main':
                        asset_type = 'logo_main'
                    elif 'logo_dark' in filename_lower or file_base == 'logo_dark':
                        asset_type = 'logo_dark'
                    elif 'logo_light' in filename_lower or file_base == 'logo_light':
                        asset_type = 'logo_light'
                    elif 'favicon' in filename_lower:
                        asset_type = 'favicon'
                    elif 'splash' in filename_lower:
                        asset_type = 'splash'
                    elif 'logo_ticket' in filename_lower or file_base == 'logo_ticket':
                        asset_type = 'logo_ticket'
                    elif 'watermark' in filename_lower:
                        asset_type = 'watermark'
                    elif 'signature' in filename_lower:
                        asset_type = 'signature'
                    elif 'placeholder' in filename_lower:
                        asset_type = 'placeholder'
                    elif 'category_' in filename_lower:
                        asset_type = 'category_image'
                    elif 'product_' in filename_lower:
                        asset_type = 'product_image'
                    elif 'button' in filename_lower or 'icon' in filename_lower:
                        asset_type = 'button_icon'
                    elif 'background' in filename_lower or 'bg' in filename_lower:
                        asset_type = 'background'
                    elif 'modal' in filename_lower:
                        asset_type = 'modal_bg'
                    elif 'logo_client' in filename_lower or file_base == 'logo_client':
                        asset_type = 'logo_client'
                    elif 'banner' in filename_lower:
                        asset_type = 'banner'
                    elif 'customer' in filename_lower:
                        asset_type = 'customer_bg'
                    else:
                        asset_type = 'other'
                    
                    # Skip if not matching selected type filter
                    if self.asset_type != 'all' and asset_type != self.asset_type:
                        continue
                    
                    assets_data.append({
                        'name': os.path.splitext(os.path.basename(file_info.filename))[0],
                        'type': asset_type,
                        'data': file_b64,
                        'filename': os.path.basename(file_info.filename),
                        'description': f'Uploaded from {self.zip_filename or "ZIP file"}'
                    })
            
            if not assets_data:
                raise UserError(_('No valid image files found in the ZIP archive.'))
            
            # Update assets using the manager model
            asset_manager = self.env['epic.asset']
            asset_manager.update_pos_assets(assets_data)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('%d assets have been successfully uploaded and processed.') % len(assets_data),
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"Error processing ZIP file: {str(e)}")
            raise UserError(_('Error processing ZIP file: %s') % str(e))