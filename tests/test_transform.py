import pytest

from src.transform import transform_crimes, transform_raw

model_input = [{
    "id": "12345",
    "category": "burglary",
    "month": "2023-01",
    "location": {
        "latitude": "51.5074",
        "longitude": "-0.1278",
        "street": {"name": "Baker Street"}
    },
    "outcome_status": {"category": "investigation-complete"}
}]

model_output = [{    
    "id": "12345",
    "category": "burglary",
    "month": "2023-01",
    "latitude": "51.5074",
    "longitude": "-0.1278",
    "street": "Baker Street",
    "outcome_status": "investigation-complete"
}]

no_outcome_input = [{
    "id": "12345",
    "category": "burglary",
    "month": "2023-01",
    "location": {       
        "latitude": "51.5074",
        "longitude": "-0.1278",
        "street": {"name": "Baker Street"}
    },
    "outcome_status": None
}]

no_outcome_output = [{    
    "id": "12345",
    "category": "burglary",
    "month": "2023-01",
    "latitude": "51.5074",
    "longitude": "-0.1278",
    "street": "Baker Street",
    "outcome_status": None
}]

no_location_input = [{
    "id": "12345",
    "category": "burglary",
    "month": "2023-01",
    "location": None,
    "outcome_status": {"category": "investigation-complete"}
}]

no_location_output = [{    
    "id": "12345",
    "category": "burglary",
    "month": "2023-01",
    "latitude": None,
    "longitude": None,
    "street": None,
    "outcome_status": "investigation-complete"
}]

empty_crimes = []

def test_transform_crimes_expected():
    result = transform_crimes(model_input)
    assert result == model_output
    
def test_transform_crimes_no_outcome():
    result = transform_crimes(no_outcome_input)
    assert result == no_outcome_output
    
def test_transform_crimes_no_location():
    result = transform_crimes(no_location_input)
    assert result == no_location_output
    
def test_empty_crimes():
    result = transform_crimes(empty_crimes)
    assert result == []
    
def test_invalid_json(tmp_path, monkeypatch, caplog):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    (tmp_path / "data" / "raw" / "crimes_2023-01.json").write_text("this is not json")

    with caplog.at_level("ERROR"):
        transform_raw()

    assert "Error decoding JSON" in caplog.text
