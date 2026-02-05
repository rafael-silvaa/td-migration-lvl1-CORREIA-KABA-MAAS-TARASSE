#!/usr/bin/env python3
"""
CDC Replication app for GlobeTrotter TD 2 - Replicates bookings from MySQL to PostgreSQL
"""

import mysql.connector
import psycopg2
from mysql.connector import Error as MySQLError
from psycopg2 import Error as PostgresError
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MySQL connection parameters
MYSQL_CONFIG = {
    'host': 'gt_mysql',
    'user': 'gt_user',
    'password': 'gt_pass',
    'database': 'globetrotter',
    'port': 3306
}

# PostgreSQL connection parameters
POSTGRES_CONFIG = {
    'host': 'gt_postgres',
    'port': 5432,
    'database': 'globetrotter',
    'user': 'gt_user',
    'password': 'gt_pass'
}

def get_mysql_connection():
    """Create and return a MySQL connection"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            connection.autocommit = True
            return connection
    except MySQLError as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

def get_postgres_connection():
    """Create and return a PostgreSQL connection"""
    try:
        connection = psycopg2.connect(**POSTGRES_CONFIG)
        return connection
    except PostgresError as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        return None

def get_new_bookings_from_mysql(mysql_conn, last_id):
    """Fetch bookings from MySQL with id > last_id"""
    try:
        cursor = mysql_conn.cursor(dictionary=True)
        query = "SELECT id, customer_email, destination, departure_date, return_date, status, updated_at FROM bookings WHERE id > %s ORDER BY id"
        cursor.execute(query, (last_id,))
        bookings = cursor.fetchall()
        logger.debug(f"Query returned {len(bookings)} new bookings for last_id={last_id}")
        cursor.close()
        return bookings
    except MySQLError as e:
        logger.error(f"Error fetching bookings from MySQL: {e}", exc_info=True)
        return []

def upsert_booking_to_postgres(postgres_conn, booking):
    """Upsert a booking to PostgreSQL"""
    try:
        cursor = postgres_conn.cursor()
        query = """
        INSERT INTO bookings (id, customer_email, destination, departure_date, return_date, status, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            customer_email = EXCLUDED.customer_email,
            destination = EXCLUDED.destination,
            departure_date = EXCLUDED.departure_date,
            return_date = EXCLUDED.return_date,
            status = EXCLUDED.status,
            updated_at = EXCLUDED.updated_at
        """
        cursor.execute(query, (
            booking['id'],
            booking['customer_email'],
            booking['destination'],
            booking['departure_date'],
            booking['return_date'],
            booking['status'],
            booking['updated_at']
        ))
        postgres_conn.commit()
        cursor.close()
        return True
    except PostgresError as e:
        logger.error(f"Error upserting booking to PostgreSQL: {e}")
        postgres_conn.rollback()
        return False

def main():
    """Main CDC replication loop"""
    logger.info("Starting GlobeTrotter CDC replication service...")
    
    # Wait for MySQL and PostgreSQL to be ready
    mysql_conn = None
    postgres_conn = None
    attempt = 0
    max_attempts = 30
    
    while attempt < max_attempts:
        if not mysql_conn:
            mysql_conn = get_mysql_connection()
            if mysql_conn:
                logger.info("Connected to MySQL")
        
        if not postgres_conn:
            postgres_conn = get_postgres_connection()
            if postgres_conn:
                logger.info("Connected to PostgreSQL")
        
        if mysql_conn and postgres_conn:
            break
        
        attempt += 1
        logger.info(f"Waiting for databases... (attempt {attempt}/{max_attempts})")
        time.sleep(2)
    
    if not mysql_conn or not postgres_conn:
        logger.error("Failed to connect to databases")
        return
    
    last_processed_id = 0
    replicated_count = 0
    poll_count = 0
    
    try:
        while True:
            poll_count += 1
            
            # Verify connections are still alive
            try:
                if not mysql_conn.is_connected():
                    logger.warning("MySQL connection lost, reconnecting...")
                    mysql_conn = get_mysql_connection()
                    if not mysql_conn:
                        logger.error("Failed to reconnect to MySQL, waiting...")
                        time.sleep(5)
                        continue
            except Exception as e:
                logger.warning(f"MySQL connection check error: {e}, reconnecting...")
                mysql_conn = get_mysql_connection()
                if not mysql_conn:
                    logger.error("Failed to reconnect to MySQL")
                    time.sleep(5)
                    continue
            
            try:
                if not postgres_conn:
                    raise Exception("PostgreSQL connection is None")
                # Simple test query to verify connection
                cursor = postgres_conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
            except Exception as e:
                logger.warning(f"PostgreSQL connection error: {e}, reconnecting...")
                postgres_conn = get_postgres_connection()
                if not postgres_conn:
                    logger.error("Failed to reconnect to PostgreSQL")
                    time.sleep(5)
                    continue
            
            try:
                # Fetch new bookings from MySQL
                new_bookings = get_new_bookings_from_mysql(mysql_conn, last_processed_id)
                
                if new_bookings:
                    logger.info(f"Found {len(new_bookings)} new booking(s) to replicate")
                    
                    for booking in new_bookings:
                        if upsert_booking_to_postgres(postgres_conn, booking):
                            last_processed_id = booking['id']
                            replicated_count += 1
                            logger.info(f"Replicated booking ID {booking['id']}: {booking['customer_email']} -> {booking['destination']}")
                        else:
                            logger.warning(f"Failed to replicate booking ID {booking['id']}")
                else:
                    logger.info(f"Poll #{poll_count}: No new bookings found (last_id={last_processed_id})")
                
            except Exception as e:
                logger.error(f"Error during polling: {e}")
                time.sleep(5)
                continue
            
            # Poll interval: check for new bookings every 3 seconds
            time.sleep(3)
            
    except KeyboardInterrupt:
        logger.info(f"\nCDC replication stopped. Total bookings replicated: {replicated_count}")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
    finally:
        try:
            if mysql_conn and mysql_conn.is_connected():
                mysql_conn.close()
                logger.info("MySQL connection closed")
        except:
            pass
        
        try:
            if postgres_conn:
                postgres_conn.close()
                logger.info("PostgreSQL connection closed")
        except:
            pass

if __name__ == '__main__':
    main()
