#!/usr/bin/env python3
"""
Aplicación GUI - Iron Condor SPX Calculator
Interfaz gráfica para calcular Iron Condors sin usar consola

Autor: MiniMax Agent
Fecha: 2025-09-28
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime
from agente_iron_condor_final import AgenteIronCondorSPX

class IronCondorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Iron Condor SPX Calculator")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Crear el agente
        self.agente = AgenteIronCondorSPX()
        
        # Variables
        self.ala_var = tk.StringVar(value="25")
        self.periodo_var = tk.StringVar(value="diario")
        self.buffer_var = tk.StringVar(value="10")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', pady=10)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(
            title_frame, 
            text="🎯 IRON CONDOR SPX CALCULATOR",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Calculadora profesional de Iron Condors con datos en tiempo real",
            font=('Arial', 10),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Panel de configuración
        config_frame = tk.LabelFrame(
            main_frame, 
            text="⚙️ Configuración",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            pady=10
        )
        config_frame.pack(fill='x', pady=(0, 20))
        
        # Configuración en grid
        self.setup_config_panel(config_frame)
        
        # Botón de cálculo
        calc_button = tk.Button(
            main_frame,
            text="🚀 CALCULAR IRON CONDOR",
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            pady=10,
            command=self.calcular_iron_condor,
            cursor='hand2'
        )
        calc_button.pack(pady=10)
        
        # Panel de resultados
        self.setup_results_panel(main_frame)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="✅ Listo para calcular",
            bg='#34495e',
            fg='white',
            anchor='w',
            padx=10
        )
        self.status_label.pack(fill='x', side='bottom')
        
    def setup_config_panel(self, parent):
        """Configurar panel de parámetros"""
        
        # Ala
        tk.Label(parent, text="🔧 Ancho del Ala:", font=('Arial', 10, 'bold'), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ala_combo = ttk.Combobox(
            parent, 
            textvariable=self.ala_var,
            values=["10", "15", "20", "25"],
            state="readonly",
            width=10
        )
        ala_combo.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(parent, text="puntos", bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=5)
        
        # Período
        tk.Label(parent, text="⏱️ Período:", font=('Arial', 10, 'bold'), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        periodo_combo = ttk.Combobox(
            parent,
            textvariable=self.periodo_var,
            values=["diario", "semanal", "mensual", "anual"],
            state="readonly",
            width=10
        )
        periodo_combo.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(parent, text="(movimiento esperado)", bg='#f0f0f0').grid(row=1, column=2, sticky='w', padx=5)
        
        # Buffer
        tk.Label(parent, text="🛡️ Buffer:", font=('Arial', 10, 'bold'), bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        buffer_spin = tk.Spinbox(
            parent,
            from_=0,
            to=50,
            textvariable=self.buffer_var,
            width=10
        )
        buffer_spin.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(parent, text="puntos de seguridad", bg='#f0f0f0').grid(row=2, column=2, sticky='w', padx=5)
        
    def setup_results_panel(self, parent):
        """Configurar panel de resultados"""
        
        results_frame = tk.LabelFrame(
            parent,
            text="📊 Resultados",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        )
        results_frame.pack(fill='both', expand=True, pady=10)
        
        # Área de texto con scroll
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=20,
            width=80,
            font=('Courier', 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Mensaje inicial
        self.mostrar_mensaje_inicial()
        
    def mostrar_mensaje_inicial(self):
        """Mostrar mensaje de bienvenida"""
        mensaje = """
🎯 IRON CONDOR SPX CALCULATOR
════════════════════════════════════════════

✨ Bienvenido al calculador profesional de Iron Condors

📋 CARACTERÍSTICAS:
   • Datos en tiempo real del SPX y VIX
   • Cálculo matemáticamente correcto de IV
   • Ajuste temporal apropiado (diario/semanal/mensual)
   • Redondeo automático a múltiplos de 5
   • Buffer de seguridad configurable

🚀 INSTRUCCIONES:
   1. Selecciona el ancho del ala (10-25 puntos)
   2. Elige el período temporal (recomendado: diario)
   3. Ajusta el buffer de seguridad si deseas
   4. Haz clic en "CALCULAR IRON CONDOR"

⚡ Presiona el botón de cálculo para obtener los strikes
   optimizados basados en la volatilidad actual del mercado.

════════════════════════════════════════════
        """
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, mensaje)
        
    def calcular_iron_condor(self):
        """Ejecutar cálculo en hilo separado"""
        self.status_label.config(text="🔄 Calculando... Obteniendo datos del mercado")
        
        # Deshabilitar botón durante cálculo
        self.root.update_idletasks()
        
        # Ejecutar en thread para no bloquear UI
        thread = threading.Thread(target=self._ejecutar_calculo)
        thread.daemon = True
        thread.start()
        
    def _ejecutar_calculo(self):
        """Ejecutar el cálculo real"""
        try:
            # Obtener parámetros
            ala = int(self.ala_var.get())
            periodo = self.periodo_var.get()
            buffer = int(self.buffer_var.get())
            
            # Ejecutar cálculo
            resultado = self.agente.ejecutar_calculo_completo(
                ala=ala,
                periodo=periodo,
                buffer=buffer
            )
            
            # Mostrar resultados en UI thread
            self.root.after(0, self._mostrar_resultados, resultado)
            
        except Exception as e:
            self.root.after(0, self._mostrar_error, str(e))
            
    def _mostrar_resultados(self, resultado):
        """Mostrar los resultados en la interfaz"""
        try:
            # Limpiar área de resultados
            self.results_text.delete(1.0, tk.END)
            
            # Formatear resultados
            output = self._formatear_resultado(resultado)
            
            # Mostrar en el área de texto
            self.results_text.insert(tk.END, output)
            
            # Actualizar status
            strikes = resultado['strikes']
            self.status_label.config(
                text=f"✅ Calculado: Iron Condor {strikes['buy_put']}/{strikes['sell_put']}/{strikes['sell_call']}/{strikes['buy_call']}"
            )
            
        except Exception as e:
            self._mostrar_error(f"Error mostrando resultados: {e}")
            
    def _formatear_resultado(self, resultado):
        """Formatear el resultado para mostrar en GUI"""
        datos = resultado['datos_mercado']
        params = resultado['parametros']
        strikes = resultado['strikes']
        resumen = resultado['resumen_estrategia']
        
        output = f"""
🎯 IRON CONDOR SPX - RESULTADO CALCULADO
════════════════════════════════════════════════════════

📊 DATOS DEL MERCADO:
   📈 SPX: ${datos['spx_valor']:,.2f}
   📉 VIX: {datos['vix_valor']:.2f}%
   📅 Fecha: {datos['fecha_datos']}

⚙️ PARÁMETROS UTILIZADOS:
   🔧 Ala elegida: {params['ala_elegida']} puntos
   ⏱️ Período temporal: {params['periodo_temporal']} (factor: √{params['factor_tiempo']})
   📊 VIX original: {params['iv_original_vix']:.2f}% (anualizado)
   📊 IV anualizado: {params['iv_anualizado']:.2f} puntos
   📊 IV ajustado por tiempo: {params['iv_ajustado_tiempo']:.2f} puntos
   🛡️ Buffer agregado: +{params['buffer_agregado']} puntos
   🎯 IV final usado: {params['iv_puntos_calculado']:.2f} puntos

🎯 STRIKES DEL IRON CONDOR:
   📉 Buy Put:  ${strikes['buy_put']:,}
   📈 Sell Put: ${strikes['sell_put']:,}  ← VENDER
   📈 Sell Call: ${strikes['sell_call']:,}  ← VENDER  
   📉 Buy Call: ${strikes['buy_call']:,}

💰 ANÁLISIS DE LA ESTRATEGIA:
   📏 Rango de rentabilidad: ${strikes['sell_put']:,} - ${strikes['sell_call']:,}
   📐 Amplitud del rango: {strikes['rango_profit']} puntos
   ⬇️ Distancia a Sell Put: {resumen['distancia_spx_sell_put']:.1f} puntos
   ⬆️ Distancia a Sell Call: {resumen['distancia_spx_sell_call']:.1f} puntos
   ⚖️ Simetría: {resumen['simetria']:.1f} puntos

📋 INSTRUCCIONES DE TRADING:
   1. VENDER Put ${strikes['sell_put']:,}
   2. COMPRAR Put ${strikes['buy_put']:,}  
   3. VENDER Call ${strikes['sell_call']:,}
   4. COMPRAR Call ${strikes['buy_call']:,}

🎲 PROFIT/LOSS:
   • Máxima ganancia: Si SPX queda entre ${strikes['sell_put']:,} y ${strikes['sell_call']:,}
   • Punto de equilibrio inferior: ${strikes['sell_put']:,} + prima recibida
   • Punto de equilibrio superior: ${strikes['sell_call']:,} - prima recibida
   • Máxima pérdida: {strikes['ancho_ala']} puntos - prima recibida

════════════════════════════════════════════════════════
✅ Cálculo completado exitosamente
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
════════════════════════════════════════════════════════
        """
        
        return output
        
    def _mostrar_error(self, error_msg):
        """Mostrar error en la interfaz"""
        self.results_text.delete(1.0, tk.END)
        error_output = f"""
❌ ERROR EN EL CÁLCULO
════════════════════════════════════════════

🚨 Se produjo un error al calcular el Iron Condor:

{error_msg}

🔧 POSIBLES SOLUCIONES:
   • Verificar conexión a internet
   • Intentar nuevamente en unos segundos
   • Verificar que los parámetros sean válidos

💡 Si el error persiste, puede ser debido a:
   • Problemas con la fuente de datos (Yahoo Finance)
   • Mercados cerrados (datos pueden estar desactualizados)
   • Problemas de conectividad

🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
════════════════════════════════════════════
        """
        self.results_text.insert(tk.END, error_output)
        self.status_label.config(text=f"❌ Error: {error_msg}")
        
        # Mostrar también un popup de error
        messagebox.showerror("Error", f"Error calculando Iron Condor:\n{error_msg}")

def main():
    """Función principal"""
    try:
        root = tk.Tk()
        app = IronCondorGUI(root)
        
        # Centrar ventana
        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_width()) // 2
        y = (root.winfo_screenheight() - root.winfo_height()) // 2
        root.geometry(f"+{x}+{y}")
        
        # Ejecutar aplicación
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error iniciando la aplicación:\n{e}")

if __name__ == "__main__":
    main()