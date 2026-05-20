import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_get_inventory_returns_dict(store_client):
    inventory = store_client.get_inventory()

    assert isinstance(inventory, dict)
    assert len(inventory) > 0


@pytest.mark.regression
def test_inventory_values_are_integers(store_client):
    inventory = store_client.get_inventory()

    for key, value in inventory.items():
        assert isinstance(value, int), f"Expected int for key '{key}', got {type(value)}"
