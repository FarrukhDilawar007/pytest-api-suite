import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseClient:
    def __init__(self, base_url: str, api_key: str = "special-key"):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "api_key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _request(self, method: str, path: str, raise_on_error: bool = True, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        if raise_on_error:
            response.raise_for_status()
        return response
