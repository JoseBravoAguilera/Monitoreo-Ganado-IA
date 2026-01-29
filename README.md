# 🐄 Arquitectura IIoT para Monitoreo Ganadero y Continuidad Operacional
**Autor:** José Bravo Aguilera  
**Estatus:** Proyecto de Título - Ingeniería en Automatización y Control Industrial  
**Calificación:** Distinción Máxima (6.9)

## 🎯 Visión General
Este proyecto implementa una solución ciberfísica (OT/IT) integral para la gestión ganadera. A través de la convergencia de hardware industrial (RFID + ESP32) y herramientas avanzadas de software (Docker, IA en Python, SQL), el sistema es capaz de detectar anomalías de salud y seguridad en tiempo real, transformando datos de sensores en decisiones estratégicas.



## 🛠️ Stack Tecnológico
- **Capa Edge (OT):** ESP32, MFRC522 (RFID), C++ (PlatformIO).
- **Capa de Infraestructura:** Docker & Docker Compose (Microservicios).
- **Capa de Datos:** MySQL (Persistencia), Pandas (ETL & Analítica).
- **Cerebro de IA:** Motor de Inferencia en Python para detección de anomalías.
- **Visualización:** Grafana Dashboards para monitoreo de KPIs en tiempo real.

## 🏗️ Arquitectura del Sistema
El sistema se basa en una arquitectura de microservicios orquestada para garantizar la **Resiliencia** y la **Escalabilidad**:

1. **Adquisición (Edge):** El ESP32 procesa lecturas RFID en el pórtico, aplicando una "Whitelist" local para asegurar la supervivencia del sistema incluso sin conexión al servidor central.
2. **Procesamiento (Cerebro):** Un motor en Python recibe las tramas de datos y aplica reglas de lógica de negocio (Etología Bovina) para clasificar eventos como NORMAL, SANIDAD o CONTROL.
3. **Persistencia y Análisis:** Los datos se almacenan en MySQL con un diseño de esquema optimizado mediante índices para analítica masiva mediante Pandas.

## 📈 Metodología de Mejora Continua
Para el desarrollo de este sistema se aplicó un enfoque basado en **DMAIC** y **Lean**, buscando optimizar el flujo de tránsito de los activos biológicos y minimizar los falsos positivos en las alertas de seguridad.

## 🚀 Cómo Desplegar
El sistema está diseñado para ser "Plug & Play" mediante contenedores:

1. Clonar repositorio.
2. Configurar hardware ESP32 con el código en `/firmware`.
3. Ejecutar la infraestructura:
   ```bash
   docker-compose up -d