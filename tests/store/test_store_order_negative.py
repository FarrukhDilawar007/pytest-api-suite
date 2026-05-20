import pytest


@pytest.mark.regression
def test_get_order_nonexistent_returns_404(store_client):
    # IDs > 10 are not valid for GET per the spec
    response = store_client.get_order(999999, raise_on_error=False)
    assert response.status_code == 404


@pytest.mark.regression
def test_get_order_invalid_id_type_returns_400(store_client):
    response = store_client.get_order("not-a-number", raise_on_error=False)
    assert response.status_code in (400, 404)


@pytest.mark.regression
def test_delete_nonexistent_order_returns_404(store_client):
    response = store_client.delete_order(999999, raise_on_error=False)
    assert response.status_code == 404
