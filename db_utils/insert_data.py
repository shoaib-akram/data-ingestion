import logging
import os
from datetime import datetime

# configure logger
log_dir = 'logger'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
log_file = os.path.join(log_dir, f'log_{timestamp}.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


def insert_movie_data(json_data, connection, cursor):
    """
    Inserts movie data into the DB along with gnere data as well
    :param json_data: JSON data to insert into the DB
    :param connection: Database connection object
    :param cursor: Cursor object to execute SQL
    :return:
    """
    try:
        movie_label = None  # for logging purposes
        for record in json_data['results']['bindings']:
            try:
                imdb_id = record['imdbId']['value']
                movie_label = record.get('movieLabel', {}).get('value')
                description = record.get('description', {}).get('value')
                publication_date = record.get('publicationDate', {}).get('value')

                duration_value = record.get('duration', {}).get('value')
                genres = record['genres']['value'].split(', ')
                insert_movie(imdb_id, movie_label, description, publication_date, duration_value, connection, cursor)

                for genre in genres:
                    genre_id = insert_genre(genre, connection, cursor)
                    if genre_id:
                        try:
                            insert_movie_genre(imdb_id, genre_id, connection, cursor)
                        except Exception as e:
                            logging.error(f"Error occurred while inserting genre {genre_id}. Error: {str(e)}")
            except Exception as e:
                logging.error(f"Error occurred while inserting movie {movie_label}. Error: {str(e)}")
        return True
    except Exception as e:
        logging.error(f"Error occurred while inserting movie data. Error: {str(e.__traceback__)}")
        return False


def insert_movie(imdb_id, movie_label, description, publication_date, duration_value, connection, cursor):
    """
    Insert movie data into DB and logs the operation
    :param imdb_id: IMDb value
    :param movie_label: Movie label
    :param description: Movie description
    :param publication_date: Movie description
    :param duration_value: Movie description
    :param connection: Database connection object
    :param cursor: Cursor object to execute SQL
    :return: None
    """
    cursor.execute(
        "INSERT INTO Movies (imdbId, movieLabel, description, publicationDate, duration) "
        "VALUES (%s, %s, %s, %s, %s)",
        (
            imdb_id,
            movie_label,
            description,
            publication_date,
            duration_value,
        )
    )
    connection.commit()
    logging.info(f"Inserted movie: {imdb_id}")


def insert_genre(genre, connection, cursor):
    """
    Insert genre data into the DB and logs the operation
    :param genre: Genre value
    :param connection: Database connection object
    :param cursor: Cursor object to execute SQL
    :return: None
    """
    cursor.execute("INSERT INTO Genres (genreLabel) VALUES (%s)", (genre,))
    connection.commit()
    cursor.execute("SELECT genreId FROM Genres WHERE genreLabel = %s", (genre,))
    genre_id = cursor.fetchone()
    if genre_id:
        logging.info(f"Inserted genre: {genre} with genreId: {genre_id[0]}")
        return genre_id[0]


def insert_movie_genre(imdb_id, genre_id, connection, cursor):
    """
    Create connection between a movie and a genre
    :param imdb_id: IMDb iD
    :param genre_id: Genre ID
    :param connection: Database connection object
    :param cursor: Cursor object to execute SQL
    :return: None
    """
    cursor.execute(
        "INSERT INTO Movie_Genre (movieId, genreId) VALUES (%s, %s)",
        (imdb_id, genre_id)
    )
    connection.commit()
    logging.info(f"Inserted movie_genre for imdbId: {imdb_id} and genreId: {genre_id}")
