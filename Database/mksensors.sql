CREATE database sensordata;
CREATE USER IF NOT EXISTS 'sensors'@'localhost' IDENTIFIED by 'password';
CREATE USER IF NOT EXISTS 'sensors'@'uba3' IDENTIFIED by 'password';
GRANT ALL PRIVILEGES ON sensordata.* TO 'sensors'@'localhost';
GRANT ALL PRIVILEGES ON sensordata.* TO 'sensors'@'uba3';
USE sensordata;
CREATE TABLE sensortbl (
    event       INT(11)     NOT NULL AUTO_INCREMENT,
    sensor      VARCHAR(10) DEFAULT NULL,
    device      VARCHAR(10) DEFAULT NULL,
    devtype     VARCHAR(10) DEFAULT NULL,
    value       float       DEFAULT NULL,
    event_ts    timestamp   DEFAULT NULL,
    capture_ts  timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event)
) ENGINE=InnoDB;
