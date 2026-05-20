"""
Flask mock provider for Pact provider verification.

Implements the /pet endpoints with canned responses that satisfy
the consumer contract defined in tests/contract/consumer/test_pet_consumer.py.

Run standalone:  python -m tests.contract.provider.mock_provider
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/pet/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    return jsonify({
        "id": pet_id,
        "name": "Fluffy",
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available",
    })


@app.route("/pet", methods=["POST"])
def create_pet():
    body = request.get_json(force=True) or {}
    return jsonify({
        "id": 100,
        "name": body.get("name", "NewPet"),
        "photoUrls": body.get("photoUrls", ["https://example.com/photo.jpg"]),
        "status": body.get("status", "available"),
    })


if __name__ == "__main__":
    app.run(port=5050)
