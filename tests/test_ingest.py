from unittest.mock import Mock

import pytest
import requests

from src.ingest import fetch_crimes, save_raw


def test_save_raw(tmp_path, monkeypatch):
    
    fake_response = Mock()
    fake_response.text = '{"crimes": []}'
    date = "2023-01"
    
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "raw").mkdir(parents=True)
    
    save_raw(fake_response, date)

    expected_file = tmp_path / "data" / "raw" / "crimes_2023-01.json"

    assert expected_file.exists()
    assert expected_file.read_text() == '{"crimes": []}'


def test_fetch_crimes(monkeypatch):

    fake_response = Mock(spec=requests.Response)
    fake_response.status_code = 200
    fake_response.text = '{"crimes": []}'
    
    def mock_get(*args, **kwargs):
        return fake_response
    
    monkeypatch.setattr("requests.get", mock_get)
    
    response = fetch_crimes("2023-01")
    
    assert response.status_code == 200
    assert response.text == '{"crimes": []}'
    
def test_fetch_crimes_http_error(monkeypatch):
    
    fake_response = Mock(spec=requests.Response)
    fake_response.status_code = 404
    fake_response.raise_for_status.side_effect = requests.HTTPError("Not Found")
    
    def mock_get(*args, **kwargs):
        return fake_response
    
    monkeypatch.setattr("requests.get", mock_get)
    
    with pytest.raises(requests.HTTPError, match="Not Found"):
        fetch_crimes("2023-01")