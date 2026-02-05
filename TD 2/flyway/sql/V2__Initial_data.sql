-- Initial data for bookings table
INSERT INTO bookings (customer_email, destination, departure_date, return_date, status, updated_at) VALUES
('alice@example.com', 'Paris', '2026-03-01', '2026-03-08', 'confirmed', CURRENT_TIMESTAMP),
('bob@example.com', 'Barcelona', '2026-03-15', '2026-03-22', 'confirmed', CURRENT_TIMESTAMP),
('claire@example.com', 'Tokyo', '2026-04-01', '2026-04-15', 'pending', CURRENT_TIMESTAMP),
('david@example.com', 'New York', '2026-02-20', '2026-02-25', 'cancelled', CURRENT_TIMESTAMP);
