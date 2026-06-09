import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "service": "ntts-order-api"
    }), 200


@app.route('/api/orders', methods=['POST'])
def create_order():
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