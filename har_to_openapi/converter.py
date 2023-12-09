import json
import sys

import requests
from haralyzer import HarParser
from openapi_schema_validator import validate


def har_to_openapi(har_file_path):
    with open(har_file_path, "r", encoding="utf-8") as har_file:
        har_data = json.load(har_file)

    parser = HarParser(har_data)
    entries = parser.har_data.get("entries", [])

    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Generated API",
            "version": "1.0.0",
        },
        "paths": {},
    }

    for entry in entries:
        request = entry["request"]
        method = request["method"].lower()
        url = request["url"]

        path = url.replace("http://", "").replace("https://", "").split("/", 1)[-1]

        if path not in openapi_spec["paths"]:
            openapi_spec["paths"][path] = {}

        openapi_spec["paths"][path][method] = {
            "responses": {
                "200": {
                    "description": "Successful response",
                },
            },
        }

    return openapi_spec


def validate_openapi_spec(openapi_spec):
    schema_url = (
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/schemas/v3.0/schema.json"
    )
    schema_data = requests.get(schema_url).json()

    validate(instance=openapi_spec, schema=schema_data)

