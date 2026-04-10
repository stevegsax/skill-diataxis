# How to Handle Errors with Status Codes

## Return structured error responses

Every error response should include a JSON body with at least an `error` field:

```python
return jsonify({"error": "Item not found", "detail": "No item with id=42"}), 404
```

Clients parse the body for user-facing messages; they branch on the status code.

## Map exceptions to status codes

Register error handlers in Flask:

```python
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": str(e)}), 400

@app.errorhandler(PermissionError)
def handle_permission_error(e):
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(Exception)
def handle_unexpected(e):
    app.logger.exception("Unhandled error")
    return jsonify({"error": "Internal server error"}), 500
```

The catch-all `Exception` handler prevents stack traces from leaking to clients.

## Handle validation errors (422)

For field-level validation failures, return 422 with per-field details:

```python
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    errors = {}
    if "name" not in data:
        errors["name"] = "required"
    if "price" in data and not isinstance(data["price"], (int, float)):
        errors["price"] = "must be a number"
    if errors:
        return jsonify({"error": "Validation failed", "fields": errors}), 422
    # ... create the item
```

For what each status code means, see the [reference](../reference/codes.md).
