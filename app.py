import uuid
from datetime import datetime, timezone

from flasgger import Swagger
from flask import Flask, jsonify, request

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}
swagger = Swagger(app, config=swagger_config)

@app.route('/api/health', methods=['GET'])
def health():
    """
        Return server status
        ---
        responses:
          200:
            description: Returns the health status of the NTTS order API
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: ok
                timestamp:
                  type: string
                  example: 2026-06-10T12:00:00Z
                service:
                  type: string
                  example: ntts-order-api
        """
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "service": "ntts-order-api"
    }), 200


@app.route('/api/orders', methods=['POST'])
def create_order():
    """
        Accept order, return receipt
        ---
        parameters:
          - in: body
            name: body
            required: true
            description: JSON payload containing product details
            schema:
              type: object
              required:
                - product_name
                - quantity
                - unit_price
              properties:
                product_name:
                  type: string
                  example: Spicy Chicken Pizza
                quantity:
                  type: integer
                  example: 2
                unit_price:
                  type: number
                  format: float
                  example: 4500.00
        responses:
          200:
            description: Successfully calculated order receipt
          400:
            description: Bad input (missing or invalid fields)
        """

    data = request.get_json()

    if not data or not all(k in data for k in ("product_name", "quantity", "unit_price")):
        return jsonify({"error": "Bad Request: Missing required fields"}), 400

    try:
        qty = int(data['quantity'])
        price = float(data['unit_price'])
    except ValueError:
        return jsonify({"error": "Bad Request: Invalid data types for quantity or unit_price"}), 400


    total = qty * price


    receipt = {
        "status": "success",
        "receipt": {
            "order_id": str(uuid.uuid4()),
            "product_name": data['product_name'],
            "quantity": qty,
            "unit_price": price,
            "total": total,
            "currency": "NGN"
        }
    }

    return jsonify(receipt), 200

if __name__ == '__main__':
    app.run(debug=True)