import logging
from datetime import datetime
from pathlib import Path
import time

import requests
from dateutil.relativedelta import relativedelta

import src.logger

logger = logging.getLogger(__name__)

def fetch_crimes(date: str, lat: float = 51.75, lng: float = -1.25) -> requests.Response:
    """Fetches crime data for a given date from the UK Police API.
    
    Args:
        date (str): The date for which to fetch crime data, in the format "YYYY-MM".
        lat (float): The latitude for which to fetch crime data. Default is 51.75.
        lng (float): The longitude for which to fetch crime data. Default is -1.25.
        
    Returns:
        requests.Response: The HTTP response object containing the crime data in JSON format.
    """
    
    url = "https://data.police.uk/api/crimes-street/all-crime"
    params = {"date": date, "lat": lat, "lng": lng}
    logger.info("Fetching crime data for %s from %s", date, url)
    response = requests.get(url, params=params, timeout=30)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.error("Error fetching crime data for %s: %s", date, e)
        raise
    return response


def save_raw(response: requests.Response, date: str) -> None:
    """Saves raw crime data to a JSON file.
    
    Args:
        response (requests.Response): The HTTP response object containing the crime data in JSON format.
        date (str): The date for which to save crime data, in the format "YYYY-MM".
        
    """
    
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    with open(f"data/raw/crimes_{date}.json", "w") as f:
        f.write(response.text)
    logger.info("Saved raw data for %s to data/raw/crimes_%s.json", date, date)
    
        
def ingest(date: str, lat: float = 51.75, lng: float = -1.25) -> None:
    """Main function to ingest crime data for a given date.
    
    Args:
        date (str): The date for which to ingest crime data, in the format "YYYY-MM".
        lat (float): The latitude for which to ingest crime data. Default is 51.75.
        lng (float): The longitude for which to ingest crime data. Default is -1.25.

    """
    response = fetch_crimes(date, lat, lng)
    save_raw(response, date)
    
def get_last_updated() -> datetime:
    """Fetches the last updated date for crime data from the UK Police API.
    
    Returns:
        datetime: The last updated date for crime data.
    """
    response = requests.get("https://data.police.uk/api/crime-last-updated")
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.error("Error fetching last updated date: %s", e)
        raise
    return datetime.strptime(response.json()["date"], "%Y-%m-%d")

def ingest_time_window(months: int = 12, lat: float = 51.75, lng: float = -1.25) -> None:
    """Ingests crime data for a specified number of past months.
    
    Args:
        months (int): The number of past months to ingest data for. Default is 12.
        lat (float): The latitude for which to ingest crime data. Default is 51.75.
        lng (float): The longitude for which to ingest crime data. Default is -1.25.
    """
    latest = get_last_updated()
    for i in range(months):
        date = (latest - relativedelta(months=i)).strftime("%Y-%m")
        ingest(date, lat, lng)
        time.sleep(1)

if __name__ == "__main__":
    ingest_time_window()