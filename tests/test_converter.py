import json
import tempfile
from unittest import mock

import pytest
from openapi_schema_validator import ValidationError

from your_module import har_to_openapi, validate_openapi_spec


def test_har_to_openapi():
    # Create a sample HAR file
    har_data = {
        "entries": [
            {
                "request": {
                    "method": "GET",
                    "url": "https://api.example.com/users",
                },
                "response": {
                    "status": 200,
                    "content": "OK",
                },
            },
            {
                "request": {
                    "method": "POST",
                    "url": "https://api.example.com/users",
                },
                "response": {
                    "status": 201,
                    "content": "Created",
                },
            },
        ]
    }

    # Write the sample HAR data to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        json.dump(har_data, temp_file)
        temp_file_path = temp_file.name

    # Call the har_to_openapi function with the temporary file path
    openapi_spec = har_to_openapi(temp_file_path)

    # Assert the expected OpenAPI spec structure
    assert "openapi" in openapi_spec
    assert "info" in openapi_spec
    assert "paths" in openapi_spec
    assert "/users" in openapi_spec["paths"]
    assert "get" in openapi_spec["paths"]["/users"]
    assert "post" in openapi_spec["paths"]["/users"]
    assert "responses" in openapi_spec["paths"]["/users"]["get"]
    assert "responses" in openapi_spec["paths"]["/users"]["post"]
    assert 200 in openapi_spec["paths"]["/users"]["get"]["responses"]
    assert 201 in openapi_spec["paths"]["/users"]["post"]["responses"]


@mock.patch("requests.get")
def test_validate_openapi_spec_valid(mock_get):
    # Create a valid OpenAPI spec
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API",
            "version": "1.0.0",
        },
        "paths": {},
    }

    # Mock the requests.get response
    mock_get.return_value.json.return_value = {"valid": "schema"}

    # Call the validate_openapi_spec function
    validate_openapi_spec(openapi_spec)

    # No assertion needed as the function should not raise an exception


@mock.patch("requests.get")
def test_validate_openapi_spec_invalid(mock_get):
    # Create an invalid OpenAPI spec
    openapi_spec = {
        "invalid": "spec",
    }

    # Mock the requests.get response
    mock_get.return_value.json.return_value = {"valid": "schema"}

    # Call the validate_openapi_spec function and expect a ValidationError
    with pytest.raises(ValidationError):
        validate_openapi_spec(openapi_spec)
