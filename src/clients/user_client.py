import requests
from src.clients.base_client import BaseClient


class UserClient(BaseClient):

    def create_user(self, payload: dict) -> requests.Response:
        return self._request("POST", "/user", json=payload)

    def create_with_array(self, users: list[dict]) -> requests.Response:
        return self._request("POST", "/user/createWithArray", json=users)

    def create_with_list(self, users: list[dict]) -> requests.Response:
        return self._request("POST", "/user/createWithList", json=users)

    def get_user(self, username: str, raise_on_error: bool = True) -> requests.Response:
        return self._request("GET", f"/user/{username}", raise_on_error=raise_on_error)

    def update_user(self, username: str, payload: dict, raise_on_error: bool = True) -> requests.Response:
        return self._request("PUT", f"/user/{username}", json=payload, raise_on_error=raise_on_error)

    def delete_user(self, username: str, raise_on_error: bool = True) -> requests.Response:
        return self._request("DELETE", f"/user/{username}", raise_on_error=raise_on_error)

    def login(self, username: str, password: str, raise_on_error: bool = True) -> requests.Response:
        return self._request(
            "GET", "/user/login",
            params={"username": username, "password": password},
            raise_on_error=raise_on_error,
        )

    def logout(self) -> requests.Response:
        return self._request("GET", "/user/logout")
