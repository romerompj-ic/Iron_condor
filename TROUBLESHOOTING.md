# 🔧 SOLUCIÓN DE PROBLEMAS - Iron Condor Web App

## ❌ Error: "Module 'plotly' not found"

### ✅ SOLUCIÓN RÁPIDA:

1. **Opción A: Usar requirements.txt actualizado**
   ```
   streamlit==1.28.1
   yfinance==0.2.18
   pandas==2.0.3
   numpy==1.24.3
   plotly==5.15.0
   ```

2. **Opción B: Usar versión mínima (sin gráficos)**
   - Reemplaza `requirements.txt` con el contenido de `requirements_minimal.txt`
   - La app funcionará pero mostrará métricas en lugar de gráficos

### 🔄 Pasos para actualizar:

1. **En GitHub:**
   - Edita el archivo `requirements.txt`
   - Copia el contenido de la Opción A
   - Guarda los cambios

2. **En Streamlit Community Cloud:**
   - Ve a tu app → Settings → "Reboot app"
   - O borra y crea la app nuevamente

---

## ❌ Error: "App won't start" / "Build failed"

### ✅ SOLUCIONES:

1. **Verifica estructura de archivos:**
   ```
   ✅ app_iron_condor_web.py
   ✅ agente_iron_condor_final.py
   ✅ requirements.txt
   ✅ README.md
   ```

2. **Verifica que el archivo principal sea:**
   - `app_iron_condor_web.py` (no main.py)

3. **Si persiste, usa requirements mínimos:**
   - Reemplaza requirements.txt con requirements_minimal.txt

---

## ❌ Error: "Data not loading" / "Yahoo Finance error"

### ✅ SOLUCIONES:

1. **Espera unos minutos** - Los servicios gratuitos tienen "cold start"
2. **Refresca la página** - Presiona F5
3. **Verifica horarios de mercado** - Funciona mejor en horarios de mercado

---

## 🚀 VERSIÓN ALTERNATIVA SIN GRÁFICOS

Si los problemas persisten, usa esta versión ultra-simple:

### requirements_minimal.txt:
```
streamlit
yfinance
pandas
numpy
```

**Ventajas:**
- ✅ 100% compatible
- ✅ Carga más rápido
- ✅ Menos dependencias
- ✅ Funciona en cualquier entorno

**Diferencias:**
- 📊 Métricas en lugar de gráficos interactivos
- 📋 Tablas en lugar de visualizaciones
- ⚡ Más ligero y estable

---

## 📞 SOPORTE

Si nada funciona, prueba estas plataformas alternativas:

1. **Render.com** - Más estable para apps complejas
2. **Railway.app** - Mejor para dependencias específicas
3. **Heroku** - Versión gratuita limitada pero robusta

¡La calculadora funcionará perfectamente una vez resueltas las dependencias! 🎯