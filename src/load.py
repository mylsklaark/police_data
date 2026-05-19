import logging
import sqlite3
from pathlib import Path

import pandas as pd

import src.logger

logger = logging.getLogger(__name__)

def load_data(dataframe: pd.DataFrame, database: str = "data/crime_data.db") -> None:
    """Loads a transformed dataframe into a SQLite database.
    
    Args:
        dataframe (pd.DataFrame): The transformed dataframe to 
            load into the database. 
            
        database (str, optional): The path to the SQLite database file. 
            Defaults to "data/crime_data.db".
    
    """
    
    logger.info("Connecting to database %s", database)
    try:
        with sqlite3.connect(database) as conn:
            dataframe.to_sql(name="crime_data",con=conn, if_exists="append", index=False)    
        conn.close()
    except sqlite3.Error as e:
        logger.exception("Error connecting to database %s: %s", database, e)
        raise
    logger.info("Loaded dataframe of length %s to database %s", len(dataframe), database)

if __name__ == "__main__":
    transformed_files = list(Path("data/processed").glob("*.csv"))
    for transformed_file in transformed_files:
        logger.info("Loading transformed data from %s", transformed_file)
        dataframe = pd.read_csv(transformed_file)
        load_data(dataframe)