import sqlite3

import pandas as pd
import pytest

from src.load import load_data


def test_load_data(tmp_path):
    
    dataframe = pd.DataFrame([{
    "id": "12345",
    "category": "burglary",
    "month": "2023-01",
    "latitude": "51.5074",
    "longitude": "-0.1278",
    "street": "Baker Street",
    "outcome_status": "investigation-complete"
    }])
    
    database = tmp_path / "test.db"
    
    load_data(dataframe, database=database)

    conn= sqlite3.connect(database)
    
    loaded_data = pd.read_sql_query("SELECT * FROM crime_data", conn)
    
    assert len(loaded_data) == 1
    assert loaded_data.iloc[0]["id"] == "12345"
    assert loaded_data.iloc[0]["category"] == "burglary"
    
    conn.close()
    
def test_load_data_db_error(monkeypatch):
    
    dataframe = pd.DataFrame([{
    "id": "12345"
    }])
    
    def mock_connect(*args, **kwargs):
        raise sqlite3.Error("Mock database connection error")
    
    monkeypatch.setattr(sqlite3, "connect", mock_connect)
    
    with pytest.raises(sqlite3.Error):
        load_data(dataframe, database="any.db")