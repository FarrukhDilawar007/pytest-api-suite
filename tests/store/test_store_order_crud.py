import pytest
from src.models.store import Order


@pytest.fixture
def placed_order(store_client, unique_id):
    payload = {
        "id": unique_id % 10 or 1,  # order IDs 1-10 are valid for GET
        "petId": 1,
        "quantity": 2,
        "status": "placed",
        "complete": False,
    }
    order = store_client.place_order(payload)
    yield order
    store_client.delete_order(order.id, raise_on_error=False)


@pytest.mark.smoke
@pytest.mark.regression
def test_place_order(store_client, unique_id):
    payload = {
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": False,
    }
    order = store_client.place_order(payload)

    assert isinstance(order, Order)
    assert order.status == "placed"
    assert order.petId == 1

    store_client.delete_order(order.id, raise_on_error=False)


@pytest.mark.regression
def test_get_order_by_id(store_client, placed_order):
    response = store_client.get_order(placed_order.id)
    order = Order.model_validate(response.json())

    assert order.id == placed_order.id
    assert order.petId == placed_order.petId


@pytest.mark.regression
def test_delete_order(store_client, unique_id):
    payload = {
        "petId": 2,
        "quantity": 1,
        "status": "placed",
        "complete": False,
    }
    order = store_client.place_order(payload)
    response = store_client.delete_order(order.id)

    assert response.status_code == 200
