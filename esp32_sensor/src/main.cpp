/*
 * PROYECTO: Arquitectura IIoT para Gestión Ganadera
 * MÓDULO: Firmware de Adquisición y Edge Computing (ESP32)
 * AUTOR: José Bravo Aguilera
 * COMPAÑEROS DE PROYECTO: Luis Lorca, Carlos Olivares
 * FECHA: Enero 2026 (Revisión de Arquitectura)
 * * FILOSOFÍA DE DISEÑO:
 * Implementación de filtrado en el borde para optimizar el ancho de banda 
 * y asegurar la continuidad operacional ante fallos de red.
 */

#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>

// --- INFRAESTRUCTURA DE HARDWARE ---
#define SS_PIN    5   // Slave Select SPI
#define RST_PIN   22  // Reset RC522
#define LED_OK    2   // Status: Activo Identificado
#define LED_ALERTA 4  // Status: Anomalía Detectada
#define BUZZER    15  // Alerta Sonora

MFRC522 rfid(SS_PIN, RST_PIN);

// --- CAPA DE DATOS EN EL BORDE (Edge Database) ---
// Representa los activos biológicos registrados en el predio.
String whitelist[] = {
  "1A D3 8B 03", "41 13 8C 03", "56 09 8C 03", 
  "F4 08 8C 03", "03 F9 8B 03", "F3 C9 5E DD",
  "B4 1A 8C 03", "87 10 8C 03", "32 58 B2 03",
  "E4 12 8C 03"
};

int total_activos = sizeof(whitelist) / sizeof(whitelist[0]);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();
  
  pinMode(LED_OK, OUTPUT);
  pinMode(LED_ALERTA, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  Serial.println(">>> NODO DE ADQUISICIÓN IIOT INICIADO <<<");
  Serial.print("Activos en Whitelist: ");
  Serial.println(total_activos);
}

void loop() {
  // Verificación de presencia de activo (Tag RFID)
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial())
    return;

  // Decodificación de Identificador Único (UID)
  String uid_capturado = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid_capturado += (rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
    uid_capturado += String(rfid.uid.uidByte[i], HEX);
  }
  uid_capturado.toUpperCase();
  uid_capturado.trim();

  // Algoritmo de Validación Local
  bool es_registrado = false;
  for (int i = 0; i < total_activos; i++) {
    if (uid_capturado == whitelist[i]) {
      es_registrado = true;
      break;
    }
  }

  // Comunicación Transversal OT/IT
  if (es_registrado) {
    digitalWrite(LED_OK, HIGH);
    // Formato de trama estandarizado para el Motor de IA en Python
    Serial.print("TELEMETRIA_DATA:"); 
    Serial.println(uid_capturado); 
  } else {
    digitalWrite(LED_ALERTA, HIGH);
    Serial.print("ALERTA_SEGURIDAD:");
    Serial.println(uid_capturado);
    
    digitalWrite(BUZZER, HIGH);
    delay(200);
    digitalWrite(BUZZER, LOW);
  }

  // Liberación de recursos y preparación para siguiente ciclo
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  delay(1500); 
  digitalWrite(LED_OK, LOW);
  digitalWrite(LED_ALERTA, LOW);
}