# Your First API with Status Codes

## Set up Flask

Create `app.py`:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

items = {"1": {"name": "Widget", "price": 9.99}}
```

## Return 200 for a successful GET

Add a route that returns an item:

```python
@app.route("/items/<item_id>")
def get_item(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200
```

Test it:

```bash
curl -i http://localhost:5000/items/1
```

```
HTTP/1.1 200 OK
Content-Type: application/json

{"name": "Widget", "price": 9.99}
```

## Return 201 for a POST that creates

```python
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item_id = str(len(items) + 1)
    items[item_id] = data
    return jsonify(data), 201
```

Test it:

```bash
curl -i -X POST -H "Content-Type: application/json" \
  -d '{"name": "Gadget", "price": 19.99}' \
  http://localhost:5000/items
```

```
HTTP/1.1 201 CREATED
Content-Type: application/json

{"name": "Gadget", "price": 19.99}
```

## See 404 for a missing item

```bash
curl -i http://localhost:5000/items/999
```

```
HTTP/1.1 404 NOT FOUND
Content-Type: application/json

{"error": "Item not found"}
```

The status code tells the client what happened without parsing the body. For
the full list of codes, see the [reference](../reference/codes.md).
