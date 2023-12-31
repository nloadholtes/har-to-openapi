import json
import sys

from converter import har_to_openapi, validate_openapi_spec

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python har_to_openapi <path-to-your-file>")
        sys.exit(1)

    har_file_path = sys.argv[1]  # 'path/to/your/file.har'

    openapi_spec = har_to_openapi(har_file_path)
    print(json.dumps(openapi_spec, indent=2))

    # Uncomment the line below to validate the generated OpenAPI spec
    # Commented out because of https://github.com/nloadholtes/har-to-openapi/issues/3
    # validate_openapi_spec(openapi_spec)
# with open(sys.argv[1] + ".openapi_spec.json", "w") as f:
#     json.dump(f, openapi_spec)
