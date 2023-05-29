import logging
from .connection import DB_NAME

# Configure logging to save logs to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('logger/data.log'),
        logging.StreamHandler()
    ]
)


def create_database_schema(connection, cursor):
    """
    Creates database schema
    :param connection: Database connection object
    :param cursor: Cursor object to execute SQL
    :return:
    """
    try:
        # Create the Genres table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Genres (
                genreId SERIAL PRIMARY KEY,
                genreLabel VARCHAR(255) NOT NULL
            )
        ''')

        # Create the Directors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Directors (
                directorId SERIAL PRIMARY KEY,
                directorLabel VARCHAR
            )
        ''')

        # Create the Movies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movies (
                imdbId VARCHAR PRIMARY KEY,
                movieLabel VARCHAR,
                description VARCHAR,
                publicationDate date,
                duration DECIMAL,
                director INTEGER REFERENCES Directors(directorId)
            )
        ''')

        # Create the Countries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Countries (
                countryId SERIAL PRIMARY KEY,
                countryLabel VARCHAR,
                movie VARCHAR REFERENCES Movies(imdbId)
            )
        ''')

        # Create the "Cast" table using double quotes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "Cast" (
                castId SERIAL PRIMARY KEY,
                castLabel VARCHAR
            )
        ''')

        # Create the Movie_Genre table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movie_Genre (
                movieId VARCHAR REFERENCES Movies(imdbId),
                genreId INTEGER REFERENCES Genres(genreId),
                PRIMARY KEY (movieId, genreId)
            )
        ''')

        # Create the Movie_Cast table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movie_Cast (
                movieId VARCHAR REFERENCES Movies(imdbId),
                castId INTEGER REFERENCES "Cast"(castId),
                PRIMARY KEY (movieId, castId)
            )
        ''')

        logging.info("Database schema creation completed successfully")
        connection.commit()
        return True
    except Exception as e:
        logging.error(f"Error occurred while creating database schema: {str(e)}")
        return False
