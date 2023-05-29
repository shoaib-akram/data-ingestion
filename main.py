import os
from json import load
import sys
import logging

from db_utils.connection import create_db_connection
from db_utils.create_schema import create_database_schema
from query.query_builder import fetch_movie_data_from_wikidata
from db_utils.insert_data import insert_movie_data


def main():
    """
    Main driver function of the app
    - Fetches data from the wiki
    - Inserts that data into the DB
    - Log every operation from insertion to errors
    :return: None
    """
    connection, cursor = None, None
    try:
        movie_data = fetch_movie_data_from_wikidata(logging)
        #  fetch movie data, if there is any issue then use static data
        if not movie_data:
            with open(os.path.join('static', 'data.json'), 'r') as data_file:
                movie_data = load(data_file)

        # Obtain the database connection and cursor
        connection, cursor = create_db_connection()
        if not connection or not cursor:
            logging.error("Exiting, couldn't connect to the DB")
            return

        create_database_schema(connection, cursor)
        insert_movie_data(movie_data, connection, cursor)
    except Exception as e:
        logging.error(f"An error occurred in {__file__}, line {sys.exc_info()[-1].tb_lineno}: {str(e)}")
    finally:
        cursor.close()
        connection.close()



if __name__ == '__main__':
    """
    Entry point of the app
    """
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
