# Epic POS Assets Manager

## Descripción

Módulo de Odoo para gestionar assets (logos, imágenes) del Point of Sale de manera segura. Permite subir archivos ZIP con múltiples assets y categorizarlos automáticamente.

## Características

- ✅ Subida de archivos ZIP con múltiples assets
- ✅ Categorización automática por nombre de archivo
- ✅ Soporte para múltiples formatos: PNG, JPG, JPEG, GIF, SVG, ICO, WebP
- ✅ Gestión segura de assets con controles de acceso
- ✅ Interfaz intuitiva de arrastrar y soltar

## Instalación

1. Copia la carpeta `epic_pos_assets` a tu directorio de addons de Odoo
2. Reinicia el servidor de Odoo
3. Ve a Apps > Actualizar lista de aplicaciones
4. Busca "Epic POS Assets" e instálalo

## Uso

### Subir Assets

1. Ve a **POS Assets > Upload Assets**
2. Selecciona un archivo ZIP con tus imágenes
3. Elige el tipo de assets (opcional, por defecto todos)
4. Haz clic en "Upload Assets"

### Gestionar Assets

1. Ve a **POS Assets > Asset Manager**
2. Visualiza, edita o elimina assets existentes
3. Añade nuevos assets manualmente si es necesario

### Convenciones de Nomenclatura

Para categorización automática, usa estos nombres:
- `logo.*` → Categorizado como Logo
- `background.*` o `bg.*` → Categorizado como Background
- `favicon.*` o `icon.*` → Categorizado como Favicon
- Otros nombres → Categorizado como Other

## Estructura del Proyecto

```
epic_pos_assets/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── pos_asset_manager.py
├── wizard/
│   ├── __init__.py
│   └── upload_assets_wizard.py
├── views/
│   ├── menu_views.xml
│   └── upload_assets_wizard_views.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

## Dependencias

- base
- point_of_sale
- web

## Versión

- **Versión**: 18.0.1.0.0
- **Compatible con**: Odoo 18.0
- **Licencia**: LGPL-3

## Soporte

Para reportar problemas o solicitar funcionalidades, contacta al equipo de Epic.