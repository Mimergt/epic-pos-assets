# Cómo Subir el Logo del POS

## Descripción

Este módulo ahora incluye una funcionalidad específica para subir el logo que aparece en la parte superior del POS (Point of Sale), junto a la barra de búsqueda.

El HTML que genera Odoo en el frontend del POS es:
```html
<div class="pos-centerheader d-flex justify-content-center overflow-hidden">
    <img class="pos-logo pos-logo mw-100" height="42" src="/web/static/img/logo.png" alt="Logo">
</div>
```

## Cómo Usar

### Opción 1: Wizard Dedicado para Logo POS

1. Ve al menú **POS Assets** → **Upload POS Logo**
2. Selecciona el archivo de imagen de tu logo
3. Haz clic en **Upload and Apply Logo**
4. Refresca el POS con **Ctrl+Shift+R** (o Cmd+Shift+R en Mac) para ver los cambios

### Opción 2: Subir en un ZIP con otros Assets

1. Ve al menú **POS Assets** → **Upload Assets**
2. Crea un archivo ZIP que contenga tu logo
3. Nombra el archivo como `logo_pos.png` (o `.jpg`, `.svg`, etc.)
4. Sube el ZIP
5. El sistema detectará automáticamente el logo del POS
6. Ve a **POS Assets** → **Asset Manager**
7. Busca el asset "Logo POS Header"
8. Haz clic en el botón **Apply Asset**
9. Refresca el POS con **Ctrl+Shift+R**

### Opción 3: Gestión Manual de Assets

1. Ve al menú **POS Assets** → **Asset Manager**
2. Haz clic en **Crear**
3. Completa los campos:
   - **Name**: "Logo POS"
   - **Asset Type**: Selecciona "Logo POS Header"
   - **File**: Sube tu archivo de imagen
4. Haz clic en **Guardar**
5. Haz clic en el botón **Apply Asset**
6. Refresca el POS con **Ctrl+Shift+R**

## Recomendaciones

- **Formato**: PNG con fondo transparente (también soporta JPG, GIF, SVG, WebP)
- **Altura**: 42px (el ancho se ajustará automáticamente manteniendo la proporción)
- **Tamaño**: Mantén el archivo lo más pequeño posible para una carga rápida
- **Compatibilidad**: Asegúrate de que el logo sea legible en diferentes tamaños

## Troubleshooting

### El logo no aparece después de subirlo

1. Asegúrate de hacer clic en **Apply Asset** después de crear/actualizar el asset
2. Refresca el navegador con **Ctrl+Shift+R** (o Cmd+Shift+R en Mac) para limpiar el caché
3. Si usas un navegador con caché agresivo, intenta en modo incógnito
4. Cierra y vuelve a abrir la sesión del POS

### El logo aparece distorsionado

- Verifica que tu imagen tenga buena calidad
- Asegúrate de que la proporción de aspecto sea apropiada
- Intenta con una imagen de 42px de altura y proporción adecuada

### No puedo ver el menú "Upload POS Logo"

- Verifica que el módulo esté correctamente instalado
- Actualiza la lista de módulos
- Verifica que tengas los permisos necesarios (group_user)

## Cambios Técnicos

Este módulo ahora incluye:

1. **Nuevo tipo de asset**: `logo_pos` - "Logo POS Header"
2. **Nuevo wizard**: `epic.wizard.pos.logo` para subida rápida
3. **Detección automática**: Los archivos nombrados `logo_pos.*` se detectan automáticamente en ZIPs
4. **Aplicación directa**: El logo se aplica al campo `logo` de la compañía, que es usado por el POS

## URL del POS

El logo aparecerá en: `https://pdv.epicdeploy.com/pos/ui?config_id=1`
