INSERT INTO restaurante (nombre, direccion) 
VALUES ('PrediMenú Anserma', 'Calle Principal #10-20');

INSERT INTO plato (nombre, precio, id_restaurante) VALUES 
('Beef Rendang', 25000, 1),
('Cendol', 8000, 1),
('Char Kway Teow', 18000, 1),
('Chicken Chop', 22000, 1),
('Chicken Rice', 15000, 1),
('Iced Lemon Tea', 5000, 1),
('Kaya Toast Set', 12000, 1),
('Laksa', 20000, 1),
('Mushroom Soup', 10000, 1),
('Nasi Lemak', 15000, 1),
('Roti Canai', 7000, 1),
('Spaghetti Carbonara', 28000, 1),
('Tandoori Chicken', 25000, 1),
('Teh Tarik', 4500, 1);

INSERT INTO usuario (username, password, id_restaurante) 
VALUES ('admin', 'admin123', 1);