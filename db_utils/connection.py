import psycopg2
import logging

DB_NAME = "wiki_app"
HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"

def create_db_connection():
    """
    Create database connection
    :return: Connection, Cursor
    """

    # Connect to the default PostgresSQL database
    default_conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD
    )
    
    default_conn.autocommit = True  # Set autocommit mode
    default_cursor = default_conn.cursor()

    try:
        # Check if the target database exists
        default_cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        database_exists = default_cursor.fetchone()
        
        if not database_exists:
            # Create the target database
            default_cursor.execute(f"CREATE DATABASE {DB_NAME}")
            default_conn.commit()
            logging.info(f"Database '{DB_NAME}' created successfully.")
        else:
            logging.info(f"Database '{DB_NAME}' already exists.")

    except psycopg2.Error as e:
        logging.error("An error occurred while creating the database.")
        logging.exception(e)

    try:
        # Connect to the target database
        conn = psycopg2.connect(
            host=HOST,
            database=DB_NAME,
            user=USER,
            password=PASSWORD
        )
        cursor = conn.cursor()
        return conn, cursor

    except psycopg2.Error as e:
        logging.error("An error occurred while connecting to the database.")
        logging.exception(e)
        return None, None
