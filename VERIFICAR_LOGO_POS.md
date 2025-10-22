# Verificación del Logo del POS

## Pasos para Verificar que el Logo se Aplicó Correctamente

### 1. Verificar que el Logo se Subió

Después de subir el logo usando el wizard:

1. Ve a **Configuración** → **Usuarios y Compañías** → **Compañías**
2. Abre tu compañía
3. Verifica que el campo **Logo** tenga la imagen que subiste
4. Si no está ahí, vuelve a subir el logo usando el wizard

### 2. Verificar la URL del Logo

En el navegador, abre esta URL (reemplaza `TU_DOMINIO` y `COMPANY_ID`):

```
https://TU_DOMINIO/web/image/res.company/COMPANY_ID/logo
```

Por ejemplo:
```
https://pdv.epicdeploy.com/web/image/res.company/1/logo
```

Deberías ver tu logo personalizado. Si ves el logo de Odoo por defecto, el logo no se ha aplicado correctamente.

### 3. Forzar la Actualización del POS

El POS cachea los recursos, por lo que necesitas:

1. **Cerrar todas las sesiones del POS**
   - Ve a: Punto de Venta → Panel → Cerrar Sesión
   - Cierra TODAS las sesiones abiertas

2. **Limpiar el caché del navegador**
   - Chrome/Edge: `Ctrl + Shift + Delete` (Windows) o `Cmd + Shift + Delete` (Mac)
   - O simplemente: `Ctrl + Shift + R` (Windows) o `Cmd + Shift + R` (Mac)

3. **Reiniciar Odoo (si tienes acceso al servidor)**
   ```bash
   sudo systemctl restart odoo
   ```
   O si usas Docker:
   ```bash
   docker restart odoo
   ```

4. **Actualizar los Assets del POS**
   - En Odoo, activa el modo desarrollador
   - Ve a: Configuración → Técnico → Vistas
   - Busca "point_of_sale"
   - Haz clic en "Regenerar Assets"

5. **Abrir una nueva sesión del POS**
   - Ve a: Punto de Venta → Panel → Nueva Sesión
   - El logo debería aparecer ahora

### 4. Si el Logo Aún No Aparece

#### Opción A: Verificar en el Inspector del Navegador

1. Abre el POS
2. Presiona `F12` para abrir las herramientas de desarrollo
3. Ve a la pestaña "Elements" o "Inspector"
4. Busca el elemento con clase `pos-logo`
5. Verifica el atributo `src` de la imagen
6. Debería ser: `/web/image/res.company/X/logo` (donde X es el ID de la compañía)
7. Si es `/web/static/img/logo.png`, el módulo no está funcionando correctamente

#### Opción B: Verificar los Logs de Odoo

En el servidor, verifica los logs:

```bash
tail -f /var/log/odoo/odoo.log | grep "POS Header Logo"
```

Deberías ver:
```
POS Header Logo applied to company [Nombre]
Updated POS config: [Nombre del POS]
Cleared Qweb cache to force logo reload
```

#### Opción C: Actualizar el Módulo Nuevamente

1. Ve a: Apps
2. Busca: "Epic POS Assets"
3. Haz clic en: **Actualizar** (Upgrade)
4. Espera a que termine la actualización
5. Cierra y reabre el POS

### 5. Solución Alternativa: Aplicar Manualmente

Si el wizard no funciona, puedes aplicar el logo manualmente:

1. Ve a: **Configuración** → **Usuarios y Compañías** → **Compañías**
2. Abre tu compañía
3. En el campo **Logo**, sube tu imagen directamente
4. Guarda
5. Limpia el caché del navegador (`Ctrl + Shift + R`)
6. Cierra y reabre el POS

### 6. Información Técnica

El logo del POS se obtiene de:
- **Backend**: Campo `logo` del modelo `res.company`
- **URL**: `/web/image/res.company/{company_id}/logo`
- **Template**: El módulo sobrescribe el template `point_of_sale.Navbar`
- **JavaScript**: Patch del componente Navbar para forzar la URL correcta

### 7. Verificación Final

Para verificar que todo funciona:

1. Sube un logo usando: **POS Assets** → **Upload POS Logo**
2. Verifica en: **Configuración** → **Compañías** que el logo se guardó
3. Visita: `https://pdv.epicdeploy.com/web/image/res.company/1/logo`
4. Limpia caché: `Ctrl + Shift + R`
5. Cierra todas las sesiones del POS
6. Abre una nueva sesión del POS
7. El logo debería aparecer correctamente

## Problema Común: Cache Persistente

El navegador o Odoo pueden estar cacheando el logo viejo. Para forzar la actualización:

```javascript
// En la consola del navegador (F12), ejecuta:
localStorage.clear();
sessionStorage.clear();
location.reload(true);
```

O simplemente usa el modo incógnito del navegador para probar.
