USE plantStatus;

-- Crea estructura de la db
CREATE TABLE equiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mac VARCHAR(100) UNIQUE NOT NULL,
    hardware VARCHAR(100),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    located VARCHAR(200) NOT NULL,
    stated SMALLINT NOT NULL
);

CREATE TABLE plantSense (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equiment_id INT,
    mac VARCHAR(100) NOT NULL,
    humedity DECIMAL(10,2) NOT NULL,
    motor_on SMALLINT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equiment_id) REFERENCES equiment(id) ON DELETE CASCADE
);
