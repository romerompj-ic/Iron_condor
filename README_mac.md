# 🍎 GUÍA COMPLETA PARA MAC - Iron Condor SPX Calculator

> **Autor:** MiniMax Agent  
> **Fecha:** 2025-09-28  
> **Sistema:** macOS

## 🚀 INSTALACIÓN SÚPER FÁCIL - 3 OPCIONES

### 📥 OPCIÓN 1: INSTALACIÓN AUTOMÁTICA (RECOMENDADA)

1. **Descarga todos los archivos** a una carpeta en tu Mac (ej: `/Users/tu_usuario/IronCondor/`)

2. **Abre Terminal** (Spotlight → buscar "Terminal")

3. **Ve a tu carpeta:**
   ```bash
   cd /Users/tu_usuario/IronCondor/
   ```

4. **Ejecuta el instalador automático:**
   ```bash
   chmod +x install_mac.sh
   ./install_mac.sh
   ```

**¡Listo!** El instalador hace todo automáticamente.

---

### 📱 OPCIÓN 2: INSTALACIÓN MANUAL PASO A PASO

**Paso 1: Verificar Python**
```bash
python3 --version
```
Si no tienes Python, descárgalo de: https://python.org/downloads/

**Paso 2: Instalar dependencias básicas**
```bash
pip3 install yfinance pandas
```

**Paso 3: (Opcional) Instalar Streamlit para interfaz web**
```bash
pip3 install streamlit plotly
```

**Paso 4: Ejecutar el launcher**
```bash
python3 launcher_mac.py
```

---

### ⚡ OPCIÓN 3: EJECUCIÓN DIRECTA

Si ya tienes Python y dependencias:

```bash
# Interfaz gráfica de escritorio
python3 app_iron_condor_gui.py

# Interfaz web (requiere streamlit)
streamlit run app_iron_condor_web.py

# Demo interactivo por consola
python3 demo_interactivo.py
```

---

## 🎯 FORMAS DE USAR EL PROGRAMA

### 1️⃣ LAUNCHER (RECOMENDADO)
```bash
python3 launcher_mac.py
```
**Ventajas:**
- Elige entre todas las interfaces
- Instala dependencias automáticamente
- Más fácil para principiantes

### 2️⃣ APLICACIÓN DE ESCRITORIO
```bash
python3 app_iron_condor_gui.py
```
**Ventajas:**
- Interfaz nativa de Mac
- No requiere navegador
- Funciona offline

### 3️⃣ APLICACIÓN WEB
```bash
streamlit run app_iron_condor_web.py
```
**Ventajas:**
- Interfaz más moderna
- Gráficos interactivos
- Visualización avanzada

### 4️⃣ CONSOLA INTERACTIVA
```bash
python3 demo_interactivo.py
```
**Ventajas:**
- Rápida y directa
- No requiere interfaz gráfica
- Ideal para usuarios avanzados

---

## 📁 ESTRUCTURA DE ARCHIVOS

Asegúrate de tener todos estos archivos en la misma carpeta:

```
📁 IronCondor/
├── 🤖 agente_iron_condor_final.py      # Motor principal (OBLIGATORIO)
├── 🚀 launcher_mac.py                  # Selector de interfaz
├── 🖥️  app_iron_condor_gui.py           # Aplicación de escritorio
├── 🌐 app_iron_condor_web.py            # Aplicación web
├── 💻 demo_interactivo.py               # Demo por consola
├── 🔧 install_mac.sh                   # Instalador automático
├── 📚 README_mac.md                    # Esta guía
└── 📖 README_corregido.md              # Documentación técnica
```

---

## 🛠️ SOLUCIÓN DE PROBLEMAS MAC

### ❌ "python3: command not found"
**Solución:**
1. Instala Python desde https://python.org/downloads/
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia Terminal

### ❌ "pip3: command not found"
**Solución:**
```bash
# Usar pip en lugar de pip3
pip install yfinance pandas

# O instalar pip
python3 -m ensurepip --upgrade
```

### ❌ "Permission denied"
**Solución:**
```bash
# Hacer ejecutable el script
chmod +x launcher_mac.py

# O usar con Python
python3 launcher_mac.py
```

### ❌ "No module named 'agente_iron_condor_final'"
**Solución:**
- Verifica que todos los archivos estén en la misma carpeta
- Ejecuta desde la carpeta correcta:
```bash
pwd  # Verificar ubicación actual
ls   # Verificar que están todos los archivos .py
```

### ❌ "SSL Certificate Error"
**Solución:**
```bash
# Instalar certificados SSL
/Applications/Python\ 3.x/Install\ Certificates.command
```

### ❌ Error con Streamlit
**Solución:**
```bash
# Reinstalar streamlit
pip3 uninstall streamlit
pip3 install streamlit plotly
```

---

## 🎮 GUÍA RÁPIDA DE USO

### Primer Uso:
1. **Abre Terminal**
2. **Ve a tu carpeta:** `cd /Users/tu_usuario/IronCondor/`
3. **Ejecuta:** `python3 launcher_mac.py`
4. **Elige la interfaz** que prefieras
5. **Configura los parámetros** (Ala: 25, Período: diario)
6. **Haz clic en "Calcular"**

### Uso Posterior:
- **Opción fácil:** Doble clic en `iron_condor_launcher.command` (si instalaste automáticamente)
- **Terminal:** `python3 launcher_mac.py`

---

## 📊 EJEMPLO DE RESULTADO

**Configuración típica:**
- **Ala:** 25 puntos
- **Período:** Diario
- **Buffer:** 10 puntos

**Resultado esperado:**
```
SPX: $6,643.70
VIX: 15.29%
IV Final: 73.99 puntos

Iron Condor:
Buy Put:  $6,570
Sell Put: $6,595
Sell Call: $6,715
Buy Call: $6,740

Rango: 120 puntos (REALISTA)
```

---

## 🔧 PERSONALIZACIÓN AVANZADA

### Cambiar período por defecto:
Edita `agente_iron_condor_final.py`, línea:
```python
self.periodo_default = 'diario'  # Cambiar a 'semanal', 'mensual', etc.
```

### Cambiar alas disponibles:
Edita `agente_iron_condor_final.py`, línea:
```python
self.alas_permitidas = [10, 15, 20, 25]  # Agregar más valores
```

---

## 📋 CHECKLIST DE VERIFICACIÓN

- [ ] Python 3.8+ instalado
- [ ] Todos los archivos .py en la misma carpeta
- [ ] Dependencias instaladas (`yfinance`, `pandas`)
- [ ] Conexión a internet activa
- [ ] Terminal puede ejecutar `python3`

---

## 🆘 SOPORTE

### Comando de diagnóstico:
```bash
python3 -c "
import sys
print('Python:', sys.version)
try:
    import yfinance, pandas, tkinter
    print('✅ Dependencias: OK')
except ImportError as e:
    print('❌ Falta:', e)
"
```

### Reinstalación limpia:
```bash
# Eliminar cache
pip3 cache purge

# Reinstalar todo
pip3 install --upgrade yfinance pandas streamlit plotly
```

---

## 🎉 ¡LISTO PARA USAR!

Una vez instalado, puedes calcular Iron Condors profesionales con datos en tiempo real del SPX. 

**El sistema está optimizado para movimiento diario, produciendo rangos realistas de ~120-200 puntos.**

**¡Feliz trading!** 🚀📈

---

**Desarrollado por MiniMax Agent** | **Versión 1.1 Corregida** | **2025-09-28**