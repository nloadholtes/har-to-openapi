# har-to-openapi
Python tool to create OpenAPI specs from HAR files

## Why

Sometimes it is not practical to test your code against your target server.

And typically there will not be any formal specification of the API on that server.

BUT! You can capture interactions with the server in a web browser by recording a HAR file from the developer's console.

This project will take that HAR file and determine what URLs were being accessed and generate an OpenAPI spec to match that.

The OpenAPI spec can then be used to generate a stub server so that you can test with confidence.

## How

_ChatGPT generated the original skeleton of this code. Then some manual testing, changes, etc._

Usage:

```bash
pip install haralyzer openapi-schema-validator

python har_to_openapi <harfile>
```

## Limitations

Your HAR file will only know about the endpoints that you access. It is very possible that the server supports many, many more endpoints than are exposed via the UI. So most likely the OpenAPI spec that is generated will be a subset of what the server actually supports.

In some cases this will not be a problem: for example if you only need to test those endpoints.

## Contributing

Please feel free to open an Issue or PR on [github](https://github.com/nloadholtes/har-to-openapi).

