# PROYECTO: Sistema Integrado de Gestión Ganadera IIoT
# AUTOR: José Bravo Aguilera (Ingeniero en Automatización)
# MÓDULO: Analítica de Continuidad Operacional (Capa IT)

import pandas as pd
from sqlalchemy import create_engine
import os
import sys

def ejecutar_pipeline_kpi():
    """
    Extrae, transforma y analiza datos de sensores para la toma de decisiones.
    Aplica conceptos de mejora continua para detectar ineficiencias en el proceso.
    """
    # Configuración de red con visión de Arquitecto (Entorno Híbrido)
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = "3306"
    DB_USER = "root"
    DB_PASS = "admin"
    DB_NAME = "CONTROL_GANADERO"

    url_conexion = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        motor = create_engine(url_conexion)
        print(f"\n--- 🛰️ CONECTANDO A INFRAESTRUCTURA DE DATOS: {DB_HOST} ---")

        # Query de extracción técnica
        # Priorizamos eficiencia cargando solo dimensiones críticas
        query = "SELECT animal_id, fecha, tipo_alerta, duracion_lectura FROM sensores_ganado"
        
        df = pd.read_sql(query, motor)

        if df.empty:
            print("[⚠️] Advertencia: El Data Lake está vacío. Verifique conectividad de los sensores.")
            return

        print(f"[✅] Telemetría recuperada exitosamente. Procesando {len(df)} eventos activos.")

        # --- CAPA DE INTELIGENCIA DE NEGOCIOS (KPIs) ---
        # Analizamos la eficiencia de tránsito y sanidad por categoría
        metricas_continuidad = df.groupby('tipo_alerta')['duracion_lectura'].agg(['mean', 'max', 'count'])
        
        # Renombramos para lenguaje de Alta Gerencia / Planta Industrial
        metricas_continuidad.columns = ['Latencia Promedio (s)', 'Pico Máximo (s)', 'Frecuencia de Eventos']

        print("\n" + "="*50)
        print("📊 REPORTE DE CONTINUIDAD OPERACIONAL")
        print("="*50)
        print(metricas_continuidad)

        # --- ANÁLISIS DE RESILIENCIA Y SEGURIDAD ---
        # Filtro de anomalías basado en el motor de IA
        eventos_criticos = df[df['tipo_alerta'].str.contains('ALERTA', na=False)].shape[0]
        tasa_fallo = (eventos_criticos / len(df)) * 100

        print(f"\n[KPI ESTRATÉGICO] Tasa de Anomalías en Proceso: {tasa_fallo:.2f}%")
        
        if tasa_fallo > 15:
            print("🔴 ALERTA: La tasa de anomalías supera el umbral de resiliencia operativa.")
        else:
            print("🟢 STATUS: Proceso estable bajo parámetros de control industrial.")

    except Exception as error:
        print(f"\n[CRITICAL ERROR] Fallo en el Pipeline de Datos: {error}")
        sys.exit(1)

if __name__ == "__main__":
    ejecutar_pipeline_kpi()