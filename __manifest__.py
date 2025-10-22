# -*- coding: utf-8 -*-
{
    "name": "Epic POS Assets",
    "summary": "Sube y actualiza logos/imágenes de POS y sitio desde un ZIP, de manera segura.",
    "description": """
Epic POS Assets Manager
=======================

This module allows you to:
* Upload and manage logos and images for Point of Sale
* Upload assets via ZIP files for bulk processing
* Categorize assets by type (logo, background, favicon, etc.)
* Secure asset management with proper access controls

Features:
---------
* Drag & drop ZIP file upload
* Automatic asset categorization based on filename
* Support for multiple image formats (PNG, JPG, GIF, SVG, ICO, WebP)
* Asset versioning and management
    """,
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "author": "Epic",
    "website": "https://www.epic.com",
    "license": "LGPL-3",
    "depends": ["base", "point_of_sale", "web"],
    "data": [
        "views/epic_asset_views.xml",
        "views/epic_wizard_views.xml",
        "views/actions_menus.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "epic_pos_assets/static/src/app/navbar/navbar.js",
            "epic_pos_assets/static/src/app/navbar/navbar.xml",
        ],
    },
    "demo": [],
    "external_dependencies": {
        "python": [],
    },
    "application": False,
    "installable": True,
    "auto_install": False,
}
