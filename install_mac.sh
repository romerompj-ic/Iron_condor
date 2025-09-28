#!/bin/bash
# Instalador Automático para Mac - Iron Condor SPX Calculator
# Autor: MiniMax Agent
# Fecha: 2025-09-28

echo "🎯 IRON CONDOR SPX CALCULATOR - INSTALADOR PARA MAC"
echo "=================================================="
echo ""

# Función para mostrar mensajes coloridos
show_success() {
    echo "✅ $1"
}

show_error() {
    echo "❌ $1"
}

show_info() {
    echo "ℹ️  $1"
}

show_warning() {
    echo "⚠️  $1"
}

# Verificar Python
echo "🔍 Verificando instalación de Python..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    show_success "Python encontrado: $python_version"
else
    show_error "Python 3 no está instalado"
    show_info "Por favor instala Python desde https://python.org/downloads/"
    exit 1
fi

# Verificar pip
echo ""
echo "🔍 Verificando pip..."
if command -v pip3 &> /dev/null; then
    show_success "pip3 encontrado"
    pip_cmd="pip3"
elif command -v pip &> /dev/null; then
    show_success "pip encontrado"
    pip_cmd="pip"
else
    show_error "pip no está disponible"
    exit 1
fi

# Instalar dependencias básicas
echo ""
echo "📦 Instalando dependencias básicas..."
$pip_cmd install yfinance pandas --quiet

if [ $? -eq 0 ]; then
    show_success "Dependencias básicas instaladas"
else
    show_error "Error instalando dependencias básicas"
    exit 1
fi

# Preguntar por Streamlit (opcional)
echo ""
read -p "🌐 ¿Quieres instalar Streamlit para la interfaz web? (y/n): " install_streamlit

if [[ $install_streamlit =~ ^[Yy]$ ]]; then
    echo "📦 Instalando Streamlit y Plotly..."
    $pip_cmd install streamlit plotly --quiet
    
    if [ $? -eq 0 ]; then
        show_success "Streamlit instalado correctamente"
    else
        show_warning "Error instalando Streamlit (puedes instalarlo después)"
    fi
fi

# Crear script ejecutable para el launcher
echo ""
echo "🔧 Configurando launcher..."

cat > iron_condor_launcher.command << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 launcher_mac.py
EOF

chmod +x iron_condor_launcher.command

show_success "Launcher configurado: iron_condor_launcher.command"

# Crear alias para terminal (opcional)
echo ""
read -p "💻 ¿Quieres crear un alias para ejecutar desde terminal? (y/n): " create_alias

if [[ $create_alias =~ ^[Yy]$ ]]; then
    shell_config=""
    
    if [ -f ~/.zshrc ]; then
        shell_config="$HOME/.zshrc"
    elif [ -f ~/.bash_profile ]; then
        shell_config="$HOME/.bash_profile"
    elif [ -f ~/.bashrc ]; then
        shell_config="$HOME/.bashrc"
    fi
    
    if [ ! -z "$shell_config" ]; then
        echo "" >> "$shell_config"
        echo "# Iron Condor SPX Calculator" >> "$shell_config"
        echo "alias ironcondor='cd \"$(pwd)\" && python3 launcher_mac.py'" >> "$shell_config"
        
        show_success "Alias 'ironcondor' agregado a $shell_config"
        show_info "Reinicia terminal o ejecuta 'source $shell_config' para usar el alias"
    else
        show_warning "No se pudo determinar el archivo de configuración del shell"
    fi
fi

# Crear script de prueba rápida
echo ""
echo "🧪 Creando script de prueba..."

cat > test_installation.py << 'EOF'
#!/usr/bin/env python3
"""Script de prueba para verificar la instalación"""

try:
    print("🧪 Probando importaciones...")
    
    # Probar agente principal
    from agente_iron_condor_final import AgenteIronCondorSPX
    print("✅ agente_iron_condor_final: OK")
    
    # Probar dependencias
    import yfinance
    print("✅ yfinance: OK")
    
    import pandas
    print("✅ pandas: OK")
    
    # Probar tkinter
    import tkinter
    print("✅ tkinter: OK")
    
    # Probar streamlit (opcional)
    try:
        import streamlit
        print("✅ streamlit: OK")
    except ImportError:
        print("⚠️  streamlit: No instalado (opcional)")
    
    # Probar el agente
    print("\n🎯 Probando el agente...")
    agente = AgenteIronCondorSPX()
    print("✅ Agente creado correctamente")
    
    print("\n🎉 ¡INSTALACIÓN EXITOSA!")
    print("📋 Todo está listo para usar")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 Revisa la instalación de dependencias")

input("\n👉 Presiona Enter para continuar...")
EOF

chmod +x test_installation.py

# Ejecutar prueba
echo ""
echo "🧪 Ejecutando prueba de instalación..."
python3 test_installation.py

# Instrucciones finales
echo ""
echo "🎉 ¡INSTALACIÓN COMPLETADA!"
echo "========================="
echo ""
echo "📋 FORMAS DE EJECUTAR EL PROGRAMA:"
echo ""
echo "1️⃣  DOBLE CLIC:"
echo "   👆 Haz doble clic en: iron_condor_launcher.command"
echo ""
echo "2️⃣  TERMINAL:"
if [[ $create_alias =~ ^[Yy]$ ]]; then
echo "   💻 Ejecuta: ironcondor"
echo "   (o reinicia terminal primero)"
else
echo "   💻 Ejecuta: python3 launcher_mac.py"
fi
echo ""
echo "3️⃣  APLICACIONES DIRECTAS:"
echo "   🖥️  Escritorio: python3 app_iron_condor_gui.py"
if [[ $install_streamlit =~ ^[Yy]$ ]]; then
echo "   🌐 Web: streamlit run app_iron_condor_web.py"
fi
echo "   💻 Consola: python3 demo_interactivo.py"
echo ""
echo "📁 ARCHIVOS PRINCIPALES:"
echo "   • agente_iron_condor_final.py (motor principal)"
echo "   • launcher_mac.py (selector de interfaz)"
echo "   • iron_condor_launcher.command (ejecutable)"
echo ""
echo "🆘 Si tienes problemas:"
echo "   • Ejecuta: python3 test_installation.py"
echo "   • Verifica que todos los archivos estén en la misma carpeta"
echo ""
show_success "¡Listo para calcular Iron Condors! 🚀"