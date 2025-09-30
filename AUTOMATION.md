# 🤖 Sistema de Automatización - Telecom & Home Digital DK

## 📅 Programación de Actualizaciones

### 🗓️ Cronograma Implementado

| Tipo | Frecuencia | Horario | Descripción |
|------|------------|---------|-------------|
| **Fiber Full Update** | Semanal | Lunes 4:00 AM UTC (6:00 AM Copenhague) | Actualización completa de todos los proveedores de Fiber |
| **Fiber Light Check** | 2x por semana | Miércoles y Viernes 2:00 PM UTC (4:00 PM Copenhague) | Verificación rápida de cambios de precios de Fiber |
| **Mobile Full Update** | Mensual | 1º de cada mes 3:00 AM UTC (5:00 AM Copenhague) | Actualización completa de todos los proveedores de Mobil |
| **TV Full Update** | Mensual | 1º de cada mes 3:00 AM UTC (5:00 AM Copenhague) | Actualización completa de todos los proveedores de TV |
| **Manual QA** | Mensual | Manual | Revisión manual de datos clave |

### ⚙️ Workflows de GitHub Actions

#### 1. **Weekly Full Update** (`scraper-schedule.yml`)
- **Trigger**: Automático (cron) + Manual
- **Funciones**:
  - Scraping completo de todos los proveedores
  - Detección de cambios en datos
  - Commit automático solo si hay cambios
  - Deploy automático a Vercel
  - Notificaciones de estado

#### 2. **Light Check** (`scraper-light-check.yml`)
- **Trigger**: Automático (cron) + Manual
- **Funciones**:
  - Verificación rápida de proveedores clave de Fiber
  - Detección de cambios de promociones
  - Reporte de estado sin commit automático

#### 3. **Mobile Monthly Update** (`scraper-mobil-schedule.yml`)
- **Trigger**: Automático (cron) + Manual
- **Funciones**:
  - Scraping completo de todos los proveedores de Mobil
  - Detección de cambios en datos
  - Commit automático solo si hay cambios
  - Deploy automático a Vercel
  - Notificaciones de estado

#### 4. **TV Monthly Update** (`scraper-tv-schedule.yml`)
- **Trigger**: Automático (cron) + Manual
- **Funciones**:
  - Scraping completo de todos los proveedores de TV
  - Detección de cambios en datos
  - Commit automático solo si hay cambios
  - Deploy automático a Vercel
  - Notificaciones de estado

### 🎛️ Modos de Scraping

El scraper soporta 3 modos diferentes:

#### Fiber Scraper:
```bash
# Modo completo (por defecto)
SCRAPER_TYPE=full python scrape_fiber.py

# Verificación ligera
SCRAPER_TYPE=light python scrape_fiber.py

# Modo de prueba
SCRAPER_TYPE=test python scrape_fiber.py
```

#### Mobile Scraper:
```bash
# Modo completo (por defecto)
SCRAPER_TYPE=full python scrape_mobil.py

# Verificación ligera
SCRAPER_TYPE=light python scrape_mobil.py

# Modo de prueba
SCRAPER_TYPE=test python scrape_mobil.py
```

#### TV Scraper:
```bash
# Modo completo (por defecto)
SCRAPER_TYPE=full python scrape_tv.py

# Verificación ligera
SCRAPER_TYPE=light python scrape_tv.py

# Modo de prueba
SCRAPER_TYPE=test python scrape_tv.py
```

### 🚀 Ejecución Manual

#### Desde GitHub Actions Dashboard:
1. Ve a **Actions** en el repositorio
2. Selecciona **"Fiber Internet Scraper - Weekly Update"**
3. Click **"Run workflow"**
4. Configura los parámetros:
   - **Scraper Type**: `full`, `light`, o `test`
   - **Force Update**: `true` para forzar actualización

#### Desde Terminal (desarrollo local):
```bash
cd scraper

# Scraping completo
python scrape_fiber.py

# Verificación ligera
SCRAPER_TYPE=light python scrape_fiber.py

# Modo de prueba
SCRAPER_TYPE=test python scrape_fiber.py
```

### 📊 Monitoreo y Logs

#### Logs de GitHub Actions:
- **Ubicación**: Repositorio → Actions → [Workflow Name]
- **Contenido**: 
  - Estado de scraping por proveedor
  - Número de planes encontrados
  - Errores y warnings
  - Resumen de cambios

#### Logs Locales:
- **Archivo**: `scraper/scraper.log`
- **Rotación**: Manual (recomendado limpiar semanalmente)

### 🔧 Configuración de Proveedores

#### Habilitar/Deshabilitar Proveedores:
Edita `scraper/scraper.py`:

```python
PROVIDERS = [
    {
        'name': 'Provider Name',
        'scraper': scrape_provider,
        'enabled': True  # Cambiar a False para deshabilitar
    }
]
```

#### Añadir Nuevos Proveedores:
1. Crear archivo en `scraper/providers/nuevo_provider.py`
2. Implementar función `scrape_nuevo_provider()`
3. Añadir a la lista `PROVIDERS` en `scraper.py`

### 📈 Métricas y KPIs

#### Métricas Automáticas:
- **Total de proveedores activos**
- **Número de planes por proveedor**
- **Tasa de éxito de scraping**
- **Frecuencia de cambios detectados**

#### Dashboard de Estado:
- **Frontend**: Muestra "Data opdateret: [fecha]"
- **GitHub**: Summary automático en cada workflow
- **Logs**: Historial completo de ejecuciones

### 🚨 Manejo de Errores

#### Errores Comunes:
1. **Proveedor no disponible**: Se omite y continúa con otros
2. **Cambios en estructura web**: Requiere actualización del scraper
3. **Rate limiting**: Implementar delays entre requests
4. **Certificados SSL**: Manejo automático de warnings

#### Alertas:
- **GitHub Actions**: Notificaciones automáticas en fallos
- **Logs**: Warnings para proveedores con problemas
- **Frontend**: Mensaje de error si no se pueden cargar datos

### 🔄 Evolución del Sistema

#### Fase Actual (MVP):
- ✅ Fiber: 1 actualización semanal completa + 2 verificaciones ligeras por semana
- ✅ Mobil: 1 actualización mensual completa
- ✅ TV: 1 actualización mensual completa
- ✅ 15 proveedores de Fiber activos
- ✅ 15 proveedores de Mobil activos
- ✅ 15 proveedores de TV activos
- ✅ Deploy automático a Vercel

#### Fase de Crecimiento:
- 📈 2-3 actualizaciones semanales
- 📈 Monitoreo en tiempo real de promociones
- 📈 Alertas automáticas para cambios significativos
- 📈 API endpoints para integraciones

#### Fase Avanzada:
- 🚀 Actualizaciones en tiempo real
- 🚀 Machine learning para detección de patrones
- 🚀 Integración con sistemas de afiliados
- 🚀 Dashboard administrativo

### 🛠️ Mantenimiento

#### Tareas Semanales:
- [ ] Revisar logs de scraping
- [ ] Verificar que todos los proveedores respondan
- [ ] Actualizar selectores CSS si es necesario

#### Tareas Mensuales:
- [ ] Revisión manual de precios y promociones
- [ ] Análisis de proveedores con baja tasa de éxito
- [ ] Optimización de performance del scraper
- [ ] Actualización de dependencias

#### Tareas Trimestrales:
- [ ] Evaluación de nuevos proveedores
- [ ] Revisión de estrategia de scraping
- [ ] Análisis de competencia
- [ ] Optimización de costos de infraestructura

---

## 📞 Soporte

Para problemas o preguntas sobre el sistema de automatización:
1. Revisar logs en GitHub Actions
2. Verificar estado de proveedores individuales
3. Consultar documentación del scraper en `scraper/README.md`
4. Contactar al equipo de desarrollo

**Última actualización**: Septiembre 2024
