import json
import logging
from pathlib import Path

import pandas as pd

import src.logger

logger = logging.getLogger(__name__)

def transform_crimes(crimes: list) -> list:
    """Transforms a list of raw crime dictionaries into a flattened format.
    
    Args:
        crimes (list): A list of dictionaries, each representing a crime with nested 
            location and outcome_status.
    
    Returns:
        list: A list of dictionaries, each representing a transformed crime with 
            flattened fields.
    
    """
    
    transformed = []
    for crime in crimes:
        outcome = crime.get("outcome_status")
        transformed.append({
            "id": crime.get("id"),
            "category": crime.get("category"),
            "month": crime.get("month"),
            "latitude": (crime.get("location") or {}).get("latitude"),
            "longitude": (crime.get("location") or {}).get("longitude"),
            "street": (crime.get("location") or {}).get("street", {}).get("name"),
            "outcome_status": outcome.get("category") if outcome else None
        })
    return transformed

def transform_raw() -> None:
    """Reads raw crime data from JSON files, transforms it, and saves it as CSV files.    
   
    """
    
    raw_files = list(Path("data/raw").glob("*.json"))
    if not raw_files:
        logger.warning("No raw files found in data/raw. Please run ingest.py first.")
        return
    for raw_file in raw_files:
        with open(raw_file) as f:
            logger.info("Loading raw data from %s", raw_file)
            try:
                crimes = json.load(f)
            except json.JSONDecodeError as e:
                logger.error("Error decoding JSON from %s: %s. Skipping.", raw_file, e)
                continue
            if not crimes:
                logger.warning("No crimes found in %s. Skipping.", raw_file)
                continue
            logger.info("Loaded %s crimes from %s", len(crimes), raw_file)
        
        transformed = transform_crimes(crimes)
        
        transformed_path = (raw_file.parent.parent / "processed" / raw_file.name.replace("crimes_", "transformed_")).with_suffix(".csv")
        transformed_path.parent.mkdir(parents=True, exist_ok=True)
        transformed_df = pd.DataFrame(transformed)
        transformed_df.to_csv(transformed_path, index=False)
        logger.info("Saved transformed dataframe of length %s to %s", len(transformed_df), transformed_path)


if __name__ == "__main__":
    transform_raw()