# Movie Data Management System

## Introduction

The Movie Data Management System is a Python-based project that aims to facilitate the storage and management of movie data. It provides functionality to fetch movie information from either Wikidata, and insert the data into a PostgreSQL database. The system also allows for querying and retrieval of movie data from the database.

With this system, you can easily gather comprehensive movie details such as movie labels, duration, directors, and associated genres. The project utilizes various modules to handle different aspects of the process, including establishing a database connection, creating the required database schema, inserting movie data, and fetching the data for display.

## Limitations of Wikidata Query Builder

**Limited Properties**: The API restricts fetching multiple properties, allowing retrieval of only a few specific properties such as instance ID, IMDb ID, movie label, and duration. This limitation can hinder obtaining comprehensive movie information.

**Handling Relationship**: Dealing with one-to-many relationships and many to many relationships in the data can be challenging. For instance, movies having multiple descriptions or publication dates may not align with expected data structures, making queries complex.

**Performance and Timeout**: Retrieving data from the Wikidata API can be time-consuming, especially when executing complex queries involving multiple properties and joining tables. It may result in performance issues, timeouts, and slow response times, impacting the efficiency of fetching a significant amount of data.

**Inconsistency and False Information**: The Wikidata API might occasionally provide inconsistent or inaccurate information. These inconsistencies could be in dates, labels, or other properties, making it crucial to handle and verify the data obtained from the API.

## Note
To handle potential timeouts when fetching data from the Wikidata Query Builder API, I have implemented a fallback solution using static data. This ensures a consistent response and avoids delays caused by API connectivity issues. 

The application will load the pre-defined static data if the API request fails or takes too long. This approach guarantees accessibility to data and maintains smooth functionality even when the API response is unavailable or delayed.

## Installation

### Prerequisites
- Python 3.x
- Pip3
- PostgreSQL

### Setup

1. Clone the repository

2. Navigate to the project directory

3. Create a virtual environment (optional but recommended):
  
    ```
    python3 -m venv env
    ```

4. Activate the virtual environment:
- For Windows:
  ```
  .\env\Scripts\activate
  ```
- For Unix/Linux:
  ```
  source env/bin/activate
  ```

5. Install the required packages from the `requirements.txt` file:
    ```
     pip3 install -r requirements.txt
   ```

6. Update postgres environment variable on `connection.py` as per your setup
4. Run command on main directory "python3 main.py" to run project


## Usage

To use the Movie Data Management System, follow these steps:

1. Fetch movie data from either Wikidata or a local data file.
2. If fetching from Wikidata is unsuccessful, ensure you have a valid `data.json` file in the `static` directory containing movie data.
3. Configure the PostgreSQL database connection details in the `db_utils/connection.py` file.
4. Run `python3 main.py`
5. The system will create the required database schema, insert the movie data into the database.

