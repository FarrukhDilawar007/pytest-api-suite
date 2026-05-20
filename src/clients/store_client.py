import requests
from src.clients.base_client import BaseClient
from src.models.store import Order


class StoreClient(BaseClient):

    def get_inventory(self) -> dict:
        r = self._request("GET", "/store/inventory")
        return r.json()

    def place_order(self, payload: dict) -> Order:
        r = self._request("POST", "/store/order", json=payload)
        return Order.model_validate(r.json())

    def get_order(self, order_id: int, raise_on_error: bool = True) -> requests.Response:
        return self._request("GET", f"/store/order/{order_id}", raise_on_error=raise_on_error)

    def delete_order(self, order_id: int, raise_on_error: bool = True) -> requests.Response:
        return self._request("DELETE", f"/store/order/{order_id}", raise_on_error=raise_on_error)
