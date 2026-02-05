-- Create bookings table in MySQL
CREATE TABLE IF NOT EXISTS bookings (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  customer_email VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  departure_date DATE NOT NULL,
  return_date DATE NOT NULL,
  status VARCHAR(50) NOT NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert initial test data
INSERT INTO bookings (customer_email, destination, departure_date, return_date, status, updated_at) VALUES
('alice@example.com', 'Paris', '2026-03-01', '2026-03-08', 'confirmed', CURRENT_TIMESTAMP),
('bob@example.com', 'Barcelona', '2026-03-15', '2026-03-22', 'confirmed', CURRENT_TIMESTAMP),
('claire@example.com', 'Tokyo', '2026-04-01', '2026-04-15', 'pending', CURRENT_TIMESTAMP),
('david@example.com', 'New York', '2026-02-20', '2026-02-25', 'cancelled', CURRENT_TIMESTAMP);
