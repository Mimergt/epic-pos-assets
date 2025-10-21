# Debugging Favicon en Epic POS Assets

## Estado Actual
- ✅ Módulo instalado sin errores
- ✅ Se puede subir assets vía ZIP
- ✅ Botón "Apply Asset" marca como aplicado
- ❌ **PROBLEMA**: El favicon no se aplica realmente al sistema

## Información del Servidor
- **Odoo Version**: 18.0-20250807
- **Container**: `9ee90548d3f0`
- **Database**: `odoo`
- **URL**: https://pdv.epicdeploy.com

## Lo que Hemos Intentado

### 1. Primer Intento - Campo directo (FALLÓ)
```python
company.write({'favicon': self.file_data})
```
**Error**: `Invalid field 'favicon' on model 'res.company'`

### 2. Segundo Intento - ir.attachment (ACTUAL)
```python
Attachment = self.env['ir.attachment']
existing_favicon = Attachment.search([
    ('name', '=', 'web.favicon'),
    ('res_model', '=', 'res.company'),
    ('res_id', '=', company.id)
], limit=1)

attachment_vals = {
    'name': 'web.favicon',
    'datas': self.file_data,
    'res_model': 'res.company',
    'res_id': company.id,
    'type': 'binary',
}

if existing_favicon:
    existing_favicon.write(attachment_vals)
else:
    Attachment.create(attachment_vals)
```
**Resultado**: No da error pero el favicon no aparece en el navegador

## Comandos de Diagnóstico Necesarios

Ejecutar en el servidor Linode para entender cómo Odoo maneja el favicon:

```bash
# 1. Entrar al shell de Odoo
docker exec -it odoo /usr/bin/odoo shell -d odoo

# Dentro del shell, ejecutar:
# Ver compañía
company = env['res.company'].search([], limit=1)
print(f"Company: {company.name}, ID: {company.id}")
print(f"Has logo: {bool(company.logo)}")

# Ver todos los campos disponibles en res.company
fields = env['ir.model.fields'].search([('model', '=', 'res.company')])
logo_fields = [f.name for f in fields if 'logo' in f.name or 'icon' in f.name or 'fav' in f.name]
print(f"Logo/Icon fields: {logo_fields}")

# Ver attachments existentes
attachments = env['ir.attachment'].search([('name', 'ilike', 'favicon')])
for att in attachments:
    print(f"Attachment: {att.name}, Model: {att.res_model}, ID: {att.res_id}")

# Ver nuestros assets
assets = env['epic.asset'].search([('asset_type', '=', 'favicon')])
for asset in assets:
    print(f"Asset: {asset.name}, Applied: {asset.applied}, Has data: {bool(asset.file_data)}")

# Salir del shell
exit()
```

## Posibles Soluciones a Investigar

### Opción A: Usar el campo company.logo
En Odoo, el favicon a veces se genera automáticamente del logo de la compañía:
```python
company.write({'logo': self.file_data})
```

### Opción B: Crear web_icon específico
Algunos módulos Odoo usan un campo específico:
```python
company.write({'web_icon': self.file_data})
```

### Opción C: Usar ir.attachment con URL
```python
attachment = Attachment.create({
    'name': 'favicon.ico',
    'datas': self.file_data,
    'public': True,
    'res_model': 'res.company',
    'res_id': company.id,
})
# Luego configurar la URL en algún lado
```

### Opción D: Módulo web personalizado
Es posible que necesitemos heredar el template web que genera el HTML y modificar el tag `<link rel="icon">`.

## Archivos del Módulo

### Estructura Actual
```
epic_pos_assets/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── pos_asset_manager.py    # Aquí está action_apply_asset()
├── wizard/
│   ├── __init__.py
│   └── upload_assets_wizard.py
├── views/
│   ├── epic_asset_views.xml
│   ├── epic_wizard_views.xml
│   └── actions_menus.xml
└── security/
    └── ir.model.access.csv
```

### Método Actual: action_apply_asset()
Ubicación: `models/pos_asset_manager.py` líneas ~95-140

## Próximos Pasos

1. **Ejecutar diagnóstico** en servidor para ver:
   - Qué campos tiene realmente `res.company`
   - Si existen attachments de favicon
   - Cómo están configurados

2. **Investigar en Odoo source** cómo se maneja el favicon:
   - Buscar en `/usr/lib/python3/dist-packages/odoo/addons/web`
   - Ver templates HTML que renderizan el `<head>`

3. **Ajustar el código** según lo que encontremos

4. **Considerar alternativas**:
   - ¿Necesitamos heredar un template web?
   - ¿Hay un módulo de Odoo 18 específico para esto?
   - ¿Necesitamos crear un controller HTTP?

## Comandos Rápidos del Servidor

```bash
# Actualizar módulo desde Git
cd /var/lib/docker/volumes/b662d8793caea30553517edb44bc8edefb87f2f95e3aad30234af9d524909eb2/_data/epic-pos-assets
git pull origin main
docker restart odoo

# Ver logs de Odoo
docker logs -f odoo

# Entrar al contenedor
docker exec -it odoo bash

# Shell de Odoo
docker exec -it odoo /usr/bin/odoo shell -d odoo
```

## Notas Importantes

- El favicon se cachea agresivamente en los navegadores
- Siempre hacer **Ctrl+Shift+R** (hard refresh) después de cambios
- El formato debe ser PNG o ICO válido
- El archivo debe estar en formato base64 en `file_data`

## Contacto
- Repositorio: https://github.com/Mimergt/epic-pos-assets
- Branch: main
