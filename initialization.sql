CREATE DATABASE IF NOT EXISTS ticket_db;

USE ticket_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    date DATETIME NOT NULL,
    available_tickets INT NOT NULL
);

CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    reserved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

INSERT INTO users (username, email, password) VALUES 
('david', 'david@gmail.com', 'test'),
('thierry', 'thierry@gmail.com', 'thierry'),
('julien', 'julien@gmail.com', 'julien')

INSERT INTO events (name, description, date, available_tickets) VALUES 
('Concert', 'Un super concert.', '2024-12-01 20:00:00', 100),
('Match', 'Un match excitant.', '2024-12-02 18:00:00', 200),
('Spectacle', 'Un spectacle incroyable.', '2024-12-03 15:00:00', 150),
('Conférence', 'Une conférence intéressante.', '2024-12-04 10:00:00', 50),
('Festival', 'Un festival inoubliable.', '2024-12-05 12:00:00', 300);

