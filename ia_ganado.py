# PROYECTO: Sistema de Inteligencia Bovina IIoT
# AUTOR: José Bravo Aguilera (Ingeniero en Automatización)
# MÓDULO: Motor de Inferencia en Tiempo Real

import mysql.connector
import pandas as pd
import time
import os
import random
from datetime import datetime

# --- CONFIGURACIÓN DE RED INDUSTRIAL (Docker Bridge) ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql_ganado'), # Resiliencia: busca el contenedor o local
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', 'admin'),
    'database': os.getenv('CONTROL_GANADERO', 'CONTROL_GANADERO'),
    'port': 3306
}

# --- MASTER DATA: ACTIVOS REGISTRADOS ---
# En un entorno real, esto vendría de una tabla 'animales'
REGISTRO_BIOLOGICO = {
    "CODIGO_01": "Negra", "CODIGO_02": "Panda", "CODIGO_03": "Felicia",
    "CODIGO_04": "Felita Especial", "CODIGO_05": "Lupita",
    "CODIGO_06": "Mostaza", "CODIGO_07": "Ele"
}

def obtener_conexion_resiliente():
    """Implementa reintentos para asegurar Continuidad Operacional (OT)."""
    intentos = 0
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as err:
            intentos += 1
            print(f"⏳ [RELIABILITY] Intento {intentos}: Esperando DB Industrial... ({err})")
            time.sleep(5)

# --- CAPA DE INTELIGENCIA: LÓGICA DE NEGOCIO ---
def ejecutar_motor_inferencia(id_tag, duracion_seg, hora_evento):
    """
    Evalúa el estado del activo basado en reglas de comportamiento y seguridad.
    """
    # 1. Validación de Seguridad (Ciberseguridad Perimetral)
    if id_tag not in REGISTRO_BIOLOGICO:
        return "ALERTA_CONTROL", f"🚨 INTRUSO DETECTADO: Tag {id_tag} no autorizado."

    identidad = REGISTRO_BIOLOGICO[id_tag]
    
    # 2. Análisis de Bienestar Animal (Sanidad)
    if not (6 <= hora_evento.hour <= 22):
        return "ALERTA_SANIDAD", f"⚠️ {identidad}: Actividad nocturna fuera de protocolo."

    # 3. Eficiencia de Tránsito (KPI Operativo)
    # Umbral de cojera/lesión definido en 8.0 segundos
    if duracion_seg > 8.0:
        return "ALERTA_SANIDAD", f"🟠 {identidad}: Tránsito lento ({duracion_seg}s) - Revisión requerida."

    return "NORMAL", "Comportamiento dentro de parámetros"

def loop_operativo():
    """Ejecuta el ciclo de vida de captura y persistencia 24/7."""
    db = obtener_conexion_resiliente()
    cursor = db.cursor()
    
    print("\n" + "="*50)
    print("🚀 SISTEMA DE MONITOREO IIOT ACTIVADO")
    print("="*50 + "\n")
    
    try:
        while True:
            try:
                # Interfaz de entrada: Simulación de sensor RFID (ESP32)
                id_leido = "E999_INTRUSO" if random.random() < 0.05 else random.choice(list(REGISTRO_BIOLOGICO.keys()))
                duracion = round(random.uniform(1.0, 10.0), 2)
                
                # Ejecución de la lógica de Arquitectura Inteligente
                status, msg = ejecutar_motor_inferencia(id_leido, duracion, datetime.now())

                # Persistencia en la Capa IT
                sql = "INSERT INTO sensores_ganado (animal_id, tipo_alerta, diagnostico, duracion_lectura) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (id_leido, status, msg, duracion))
                db.commit()
                
                icon = "🟢" if status == "NORMAL" else "🔴"
                print(f"{icon} [{status}] {msg}")
                
                time.sleep(5) # Delay de escaneo

            except mysql.connector.Error:
                print("⚠️ [FAULT] Fallo en conexión. Iniciando protocolo de recuperación...")
                db = obtener_conexion_resiliente()
                cursor = db.cursor()

    except KeyboardInterrupt:
        print("\n🛑 Apagado de sistema por mantenimiento de usuario.")
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    loop_operativo()