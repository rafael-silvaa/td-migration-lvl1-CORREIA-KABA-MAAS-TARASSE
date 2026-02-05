#!/usr/bin/env python3
"""
Faker app for GlobeTrotter TD 2 - Generates booking data for MySQL
"""

import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime, timedelta
from faker import Faker
import logging
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()

# MySQL connection parameters
MYSQL_CONFIG = {
    'host': 'gt_mysql',
    'user': 'gt_user',
    'password': 'gt_pass',
    'database': 'globetrotter',
    'port': 3306
}

DESTINATIONS = [
    'Paris', 'Barcelona', 'Rome', 'London', 'Amsterdam',
    'Tokyo', 'Bangkok', 'Singapore', 'Sydney', 'Dubai',
    'New York', 'Los Angeles', 'Toronto', 'Mexico City', 'Rio de Janeiro',
    'Berlin', 'Madrid', 'Vienna', 'Prague', 'Istanbul'
]

STATUSES = ['pending', 'confirmed', 'cancelled']

def get_mysql_connection():
    """Create and return a MySQL connection"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            logger.info("Connected to MySQL database")
            return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

def insert_booking(cursor, customer_email, destination, departure_date, return_date, status):
    """Insert a single booking into MySQL"""
    query = """
    INSERT INTO bookings (customer_email, destination, departure_date, return_date, status, updated_at)
    VALUES (%s, %s, %s, %s, %s, NOW())
    """
    try:
        cursor.execute(query, (customer_email, destination, departure_date, return_date, status))
        return True
    except Error as e:
        logger.error(f"Error inserting booking: {e}")
        return False

def generate_booking_data():
    """Generate random booking data"""
    customer_email = fake.email()
    destination = random.choice(DESTINATIONS)
    departure_date = fake.date_between(start_date='today', end_date='+30d')
    return_date = departure_date + timedelta(days=random.randint(3, 15))
    status = random.choice(STATUSES)
    
    return customer_email, destination, departure_date, return_date, status

def main():
    """Main function - continuous booking generation"""
    logger.info("Starting GlobeTrotter data generation service...")
    
    # Wait for MySQL to be ready
    attempt = 0
    max_attempts = 30
    connection = None
    
    while attempt < max_attempts:
        connection = get_mysql_connection()
        if connection:
            break
        attempt += 1
        logger.info(f"Waiting for MySQL... (attempt {attempt}/{max_attempts})")
        time.sleep(2)
    
    if not connection:
        logger.error("Failed to connect to MySQL after multiple attempts")
        return
    
    # Generate bookings continuously
    booking_count = 0
    try:
        while True:
            cursor = connection.cursor()
            
            # Generate and insert a booking
            customer_email, destination, departure_date, return_date, status = generate_booking_data()
            
            if insert_booking(cursor, customer_email, destination, departure_date, return_date, status):
                booking_count += 1
                logger.info(f"[#{booking_count}] Inserted booking: {customer_email} -> {destination} ({status})")
                connection.commit()
            else:
                connection.rollback()
            
            cursor.close()
            
            # Wait before generating next booking (random interval between 2-5 seconds)
            wait_time = random.uniform(2, 5)
            time.sleep(wait_time)
            
    except KeyboardInterrupt:
        logger.info(f"\nData generation stopped. Total bookings generated: {booking_count}")
    except Error as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            logger.info("MySQL connection closed")

if __name__ == '__main__':
    main()
