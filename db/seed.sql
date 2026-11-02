USE padel_almagro;

-- 1) Tablas sin dependencias
INSERT INTO profesor (nombre, apellido, certificacion, telefono) VALUES
('Martín', 'Acosta', 'Instructor Nivel 2', '1100000101'),
('Lucía', 'Benítez', 'Instructor Nivel 1', '1100000102'),
('Rodrigo', 'Campos', 'Instructor Nivel 3', '1100000103'),
('Valeria', 'Domínguez', 'Instructor Nivel 2', '1100000104'),
('Nicolás', 'Ferreyra', 'Instructor Nivel 1', '1100000105');

INSERT INTO cancha (nombre, cubierta, activa) VALUES
('Cancha 1', TRUE, TRUE),
('Cancha 2', TRUE, TRUE),
('Cancha 3', FALSE, TRUE),
('Cancha 4', FALSE, TRUE),
('Cancha 5', FALSE, FALSE);

INSERT INTO tarifa (nombre, tipo_dia, hora_desde, hora_hasta, precio_hora) VALUES
('Semana mañana', 'semana', '08:00', '17:00', 8000.00),
('Semana noche', 'semana', '17:00', '23:00', 12000.00),
('Fin de semana día', 'finde', '08:00', '17:00', 10000.00),
('Fin de semana noche', 'finde', '17:00', '23:00', 14000.00),
('Feriado', 'feriado', '08:00', '23:00', 13000.00);

-- password_hash: texto de relleno, NO son contraseñas reales
INSERT INTO usuario (nombre, email, telefono, password_hash, rol) VALUES
('Admin Demo', 'admin@example.com', '1100000201', 'HASH_DE_EJEMPLO_1', 'admin'),
('Ana Gómez', 'ana.gomez@example.com', '1100000202', 'HASH_DE_EJEMPLO_2', 'cliente'),
('Luis Pérez', 'luis.perez@example.com', '1100000203', 'HASH_DE_EJEMPLO_3', 'cliente'),
('Marta Díaz', 'marta.diaz@example.com', '1100000204', 'HASH_DE_EJEMPLO_4', 'cliente'),
('Pablo Ruiz', 'pablo.ruiz@example.com', '1100000205', 'HASH_DE_EJEMPLO_5', 'cliente'),
('Sofía Torres', 'sofia.torres@example.com', '1100000206', 'HASH_DE_EJEMPLO_6', 'cliente');

INSERT INTO torneo (nombre, categoria, fecha_inicio, fecha_fin, cupo, precio_inscripcion) VALUES
('Copa Almagro Primavera', '6ta', '2026-11-14', '2026-11-15', 16, 20000.00),
('Copa Almagro Primavera', '7ma', '2026-11-21', '2026-11-22', 16, 18000.00),
('Torneo Relámpago', '5ta', '2026-11-28', '2026-11-28', 8, 15000.00),
('Torneo de Verano', '6ta', '2026-12-12', '2026-12-13', 16, 22000.00),
('Torneo de Cierre', 'Mixto', '2026-12-19', '2026-12-20', 12, 25000.00);

-- 2) Tablas con FK (los ids referenciados ya existen)
INSERT INTO clase (id_profesor, id_cancha, tipo, nivel, dia_semana, hora_inicio, hora_fin, cupo, precio) VALUES
(1, 1, 'Grupal', 'Principiante', 'lunes', '18:00', '19:00', 4, 6000.00),
(2, 2, 'Grupal', 'Intermedio', 'martes', '19:00', '20:00', 4, 6500.00),
(3, 3, 'Individual', 'Avanzado', 'miércoles', '10:00', '11:00', 1, 12000.00),
(4, 4, 'Grupal', 'Principiante', 'jueves', '20:00', '21:00', 4, 6000.00),
(5, 1, 'Grupal', 'Intermedio', 'sábado', '11:00', '12:00', 4, 6500.00);

-- 2026-11-02 es lunes, 2026-11-07 sábado, 2026-11-08 domingo
INSERT INTO reserva (id_usuario, id_cancha, id_tarifa, fecha, hora_inicio, hora_fin, estado, precio_total) VALUES
(2, 1, 2, '2026-11-02', '18:00', '19:00', 'confirmada', 12000.00),
(3, 2, 1, '2026-11-03', '10:00', '11:00', 'confirmada', 8000.00),
(4, 3, 4, '2026-11-07', '19:00', '20:00', 'pendiente', 14000.00),
(5, 1, 3, '2026-11-08', '11:00', '12:00', 'confirmada', 10000.00),
(2, 4, 2, '2026-11-05', '20:00', '21:00', 'cancelada', 12000.00),
(6, 2, 2, '2026-11-06', '19:00', '20:00', 'confirmada', 12000.00);

INSERT INTO consulta (id_usuario, nombre, email, asunto, mensaje, atendida) VALUES
(2, 'Ana Gómez', 'ana.gomez@example.com', 'Horarios', 'Quisiera saber si hay turnos libres el viernes.', TRUE),
(3, 'Luis Pérez', 'luis.perez@example.com', 'Clases', 'Hay clases para principiantes los sábados?', FALSE),
(NULL, 'Carla Ríos', 'carla.rios@example.com', 'Torneos', 'Cómo me inscribo al torneo de noviembre?', FALSE),
(NULL, 'Diego Sosa', 'diego.sosa@example.com', 'Precios', 'Hay descuento por reservas fijas?', TRUE),
(5, 'Pablo Ruiz', 'pablo.ruiz@example.com', 'Cancelación', 'Puedo cancelar una reserva con 24 horas?', FALSE);

INSERT INTO inscripcion_clase (id_usuario, id_clase, estado) VALUES
(2, 1, 'activa'),
(3, 2, 'activa'),
(4, 1, 'activa'),
(5, 4, 'cancelada'),
(6, 5, 'activa');

INSERT INTO inscripcion_torneo (id_usuario, id_torneo, estado) VALUES
(2, 1, 'confirmada'),
(3, 1, 'confirmada'),
(4, 2, 'pendiente'),
(5, 3, 'confirmada'),
(6, 4, 'pendiente');

INSERT INTO contactos (nombre, email, asunto, mensaje) VALUES
('Carla Ríos', 'carla.rios@example.com', 'Consulta', 'Quisiera saber los horarios disponibles.'),
('Diego Sosa', 'diego.sosa@example.com', 'Clases', 'Ofrecen clases para principiantes?'),
('Elena Vera', 'elena.vera@example.com', 'Torneos', 'Cuándo es el próximo torneo?'),
('Fabián Luna', 'fabian.luna@example.com', 'Precios', 'Hay descuento por reservas fijas?'),
('Gisela Mora', 'gisela.mora@example.com', 'Ubicación', 'Tienen estacionamiento?');
