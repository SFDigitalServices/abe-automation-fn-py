{
    "scriptFile": "__init__.py",
    "bindings": [
      {
        "authLevel": "anonymous",
        "type": "httpTrigger",
        "direction": "in",
        "name": "req",
        "route": "address",
        "methods": [
          "post"
        ]
      },
      {
        "type": "http",
        "direction": "out",
        "name": "$return"
      }
    ]
  }
  