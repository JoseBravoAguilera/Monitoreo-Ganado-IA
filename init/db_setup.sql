USE CONTROL_GANADERO;

-- 1. TABLA DE VACAS (El Padrón - Quiénes son)
CREATE TABLE IF NOT EXISTS GANADO (
    Id_Animal VARCHAR(50) PRIMARY KEY,
    Nombre VARCHAR(50),
    Raza VARCHAR(50) DEFAULT 'Mestiza',
    Estado_Salud VARCHAR(20) DEFAULT 'Sano'
);

-- 2. Insertamos las 6 VACAS DEL PROTOTIPO (Puedes cambiar los nombres)
INSERT INTO GANADO (Id_Animal, Nombre, Raza) VALUES
('E2001', 'Lola', 'Holstein'),
('E2002', 'Estrella', 'Jersey'),
('E2003', 'Manchas', 'Overo'),
('E2004', 'Negra', 'Angus'),
('E2005', 'Pinta', 'Clavel'),
('E2006', 'Blanca', 'Holstein')
ON DUPLICATE KEY UPDATE Nombre=Nombre; 

-- 3. TABLA DE LECTURAS (El Historial - Qué hacen)
CREATE TABLE IF NOT EXISTS LECTURA_RFID (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Fecha_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Id_Animal VARCHAR(50),
    Lugar_Lector VARCHAR(50) DEFAULT 'Comedero',
    FOREIGN KEY (Id_Animal) REFERENCES GANADO(Id_Animal)
);

-- 4. TABLA HARDWARE (Para activar la Alarma/Buzzer)
CREATE TABLE IF NOT EXISTS LECTOR_DISPOSITIVO (
    Id_Lector VARCHAR(50) PRIMARY KEY,
    Estado_Alarma INT DEFAULT 0, -- 0: Verde, 1: Rojo
    Estado_Buzzer INT DEFAULT 0  -- 0: Silencio, 1: Sonando
);

INSERT INTO LECTOR_DISPOSITIVO (Id_Lector, Estado_Alarma, Estado_Buzzer) 
VALUES ('ESP32-001', 0, 0)
ON DUPLICATE KEY UPDATE Id_Lector=Id_Lector;