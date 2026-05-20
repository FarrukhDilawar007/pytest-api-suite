import requests
from src.clients.base_client import BaseClient
from src.models.pet import Pet


class PetClient(BaseClient):

    def create_pet(self, payload: dict) -> Pet:
        r = self._request("POST", "/pet", json=payload)
        return Pet.model_validate(r.json())

    def update_pet(self, payload: dict) -> Pet:
        r = self._request("PUT", "/pet", json=payload)
        return Pet.model_validate(r.json())

    def get_pet(self, pet_id: int, raise_on_error: bool = True) -> requests.Response:
        return self._request("GET", f"/pet/{pet_id}", raise_on_error=raise_on_error)

    def delete_pet(self, pet_id: int, raise_on_error: bool = True) -> requests.Response:
        return self._request("DELETE", f"/pet/{pet_id}", raise_on_error=raise_on_error)

    def find_by_status(self, status: str | list[str]) -> list[Pet]:
        if isinstance(status, list):
            params = [("status", s) for s in status]
        else:
            params = {"status": status}
        r = self._request("GET", "/pet/findByStatus", params=params)
        return [Pet.model_validate(p) for p in r.json()]

    def find_by_status_raw(self, status: str) -> requests.Response:
        return self._request("GET", "/pet/findByStatus", raise_on_error=False, params={"status": status})

    def find_by_tags(self, tags: list[str]) -> list[Pet]:
        params = [("tags", t) for t in tags]
        r = self._request("GET", "/pet/findByTags", params=params)
        return [Pet.model_validate(p) for p in r.json()]

    def update_pet_with_form(self, pet_id: int, name: str = None, status: str = None) -> requests.Response:
        data = {}
        if name is not None:
            data["name"] = name
        if status is not None:
            data["status"] = status
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self._request("POST", f"/pet/{pet_id}", data=data, headers=headers, raise_on_error=False)

    def upload_image(
        self, pet_id: int, file_path: str, additional_metadata: str = None, raise_on_error: bool = True
    ) -> requests.Response:
        data = {}
        if additional_metadata:
            data["additionalMetadata"] = additional_metadata
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "image/jpeg")}
            r = self.session.post(
                f"{self.base_url}/pet/{pet_id}/uploadFile",
                files=files,
                data=data,
            )
        if raise_on_error:
            r.raise_for_status()
        return r
