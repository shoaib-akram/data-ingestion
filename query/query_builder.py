import requests

WIKI_DATA_URL = "https://query.wikidata.org/sparql"


def fetch_movie_data_from_wikidata(logging):
    """
    Fetch movie data using 'requests'
    :param logging: Logger object to log any errors
    :return: Movie date
    """
    query = """
        SELECT ?imdbId
            (SAMPLE(?movie) AS ?movie)
            (SAMPLE(?movieLabel) AS ?movieLabel)
            (SAMPLE(?description) AS ?description)
            (SAMPLE(?publicationDate) AS ?publicationDate)
            (SAMPLE(?duration) AS ?duration)
            (GROUP_CONCAT(DISTINCT ?genreLabel; SEPARATOR=", ") AS ?genres)
        WHERE {
            ?movie wdt:P31 wd:Q11424;         # Instance of film
                wdt:P345 ?imdbId;          # IMDb ID
                OPTIONAL { ?movie rdfs:label ?movieLabel. }
                OPTIONAL { ?movie schema:description ?description. }
                ?movie wdt:P577 ?publicationDate.   # Release date
                OPTIONAL { ?movie wdt:P2047 ?duration. }  # Duration
                OPTIONAL {
                    ?movie wdt:P136 ?genre.
                    ?genre rdfs:label ?genreLabel.
                    FILTER(LANG(?genreLabel) = "en")
                }
            FILTER(LANG(?movieLabel) = "en")   # Filter for English movie titles
            FILTER(LANG(?description) = "en")  # Filter for English descriptions
            FILTER(YEAR(?publicationDate) > 2013)
        }
        GROUP BY ?imdbId
    """

    try:
        response = requests.get(WIKI_DATA_URL, params={"format": "json", "query": query})
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logging.error("Error occurred while fetching data from Wikidata.")
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred during the request:", str(e))
