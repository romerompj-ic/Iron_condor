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
