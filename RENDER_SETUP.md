# 🚀 Configuración de Render para S3

## Problema Actual
El diagnóstico muestra que el sistema está usando **FileSystemStorage** (almacenamiento local) en lugar de **S3Boto3Storage** (S3).

## ✅ Solución: Configurar Variables de Entorno

### Paso 1: Verificar Variables Actuales
Ejecuta este comando para ver el estado actual:
```bash
python test_env.py
```

### Paso 2: Configurar Variables en Render

#### Opción A: Dashboard de Render (Recomendado)
1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Selecciona tu servicio **jewerly-catalog**
3. Ve a la pestaña **"Environment"**
4. Haz clic en **"Add Environment Variable"**
5. Agrega estas variables:

```
AWS_ACCESS_KEY_ID = tu_access_key_aqui
AWS_SECRET_ACCESS_KEY = tu_secret_key_aqui
AWS_STORAGE_BUCKET_NAME = management360
AWS_S3_REGION_NAME = us-east-2
```

#### Opción B: Render CLI
```bash
# Instalar Render CLI si no lo tienes
npm install -g render-cli

# Configurar variables
render env set AWS_ACCESS_KEY_ID tu_access_key_aqui
render env set AWS_SECRET_ACCESS_KEY tu_secret_key_aqui
render env set AWS_STORAGE_BUCKET_NAME management360
render env set AWS_S3_REGION_NAME us-east-2
```

### Paso 3: Redeploy
Después de configurar las variables:
1. Ve al dashboard de Render
2. Selecciona tu servicio
3. Haz clic en **"Manual Deploy"** → **"Deploy latest commit"**

### Paso 4: Verificar Configuración
Después del redeploy:
1. Ve a `/products/diagnostic/s3/`
2. Deberías ver:
   - ✅ **Storage Type:** `S3Boto3Storage`
   - ✅ **Bucket:** `management360`
   - ✅ **Todas las pruebas en verde**

## 🔍 Logs de Verificación

### En Desarrollo (Local)
```bash
python manage.py runserver
# Busca logs que empiecen con [S3]
```

### En Producción (Render)
```bash
# En el dashboard → Service → Logs
# O usando CLI:
render logs --app jewerly-catalog-kpoy
```

### Logs Esperados Después de la Configuración:
```
[S3] === S3 CONFIGURATION CHECK ===
[S3] AWS_ACCESS_KEY_ID: 'AKIA...' (length: 20)
[S3] AWS_SECRET_ACCESS_KEY: '***wxyz' (length: 40)
[S3] AWS_STORAGE_BUCKET_NAME: 'management360'
[S3] AWS_S3_REGION_NAME: 'us-east-2'
[S3] ✅ All credentials present - configuring S3 storage
[S3] ✅ S3 storage configured successfully
[S3] Media URL: https://management360.s3.amazonaws.com/
```

## 🐛 Troubleshooting

### Si Sigue Usando Local Storage:
1. **Verifica las variables:**
   ```bash
   python test_env.py
   ```

2. **Revisa los logs de inicio:**
   ```
   [S3] ❌ AWS_ACCESS_KEY_ID is missing or empty
   ```

3. **Verifica en Render:**
   - Las variables deben estar en **Environment** (no en Secrets)
   - Asegúrate de que no tengan espacios extra
   - Redeploy después de cambiarlas

### Si Hay Errores de Conexión S3:
1. **Verifica credenciales de AWS:**
   - Access Key debe ser válida
   - Secret Key debe ser correcta
   - Usuario IAM debe tener permisos para el bucket

2. **Verifica bucket:**
   - Bucket `management360` debe existir
   - Región debe ser `us-east-2`
   - Política del bucket debe permitir acceso

## 📋 Checklist Final

- [ ] Variables de entorno configuradas en Render
- [ ] Redeploy completado
- [ ] Diagnóstico muestra S3Boto3Storage
- [ ] Subida de imágenes funciona
- [ ] URLs de imágenes apuntan a S3
- [ ] Logs muestran configuración correcta

## 🎯 Resultado Esperado

Después de la configuración correcta:
- ✅ **Storage:** S3Boto3Storage
- ✅ **URLs:** `https://management360.s3.amazonaws.com/...`
- ✅ **Archivos:** Se guardan en S3
- ✅ **Acceso:** Público (con política correcta del bucket)

¡El sistema estará completamente configurado para producción con S3!