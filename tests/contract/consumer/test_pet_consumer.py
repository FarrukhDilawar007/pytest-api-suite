"""
Pact consumer contract tests.

Defines what the PetConsumer expects from the PetProvider.
Writes pact JSON to /pacts directory for provider verification.

Note: requires pact-python FFI (pact_ffi). On Windows with Python 3.13 the
DLL may fail to load — tests are skipped in that case and run in Linux CI.
"""
import pytest

try:
    from pact import Consumer, Provider, Like, EachLike, Term
    _PACT_AVAILABLE = True
except (ImportError, OSError):
    _PACT_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _PACT_AVAILABLE,
    reason="pact-python FFI not available on this platform — runs in CI (Linux)",
)

PACT_DIR = "pacts"
PACT_HOST = "localhost"
PACT_PORT = 1235


@pytest.fixture(scope="module")
def pact():
    p = Consumer("PetConsumer").has_pact_with(
        Provider("PetProvider"),
        host_name=PACT_HOST,
        port=PACT_PORT,
        pact_dir=PACT_DIR,
        log_dir="logs",
    )
    p.start_service()
    yield p
    p.stop_service()


@pytest.mark.contract
def test_get_pet_by_id_contract(pact):
    expected_pet = {
        "id": Like(1),
        "name": Like("Fluffy"),
        "photoUrls": EachLike("https://example.com/photo.jpg"),
        "status": Term(r"available|pending|sold", "available"),
    }

    (
        pact.given("a pet with id 1 exists")
        .upon_receiving("a GET request for pet 1")
        .with_request("GET", "/pet/1", headers={"api_key": "special-key"})
        .will_respond_with(200, body=expected_pet)
    )

    import requests
    with pact:
        response = requests.get(
            f"http://{PACT_HOST}:{PACT_PORT}/pet/1",
            headers={"api_key": "special-key"},
        )
        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        assert "name" in body


@pytest.mark.contract
def test_create_pet_contract(pact):
    new_pet = {
        "name": Like("NewPet"),
        "photoUrls": EachLike("https://example.com/photo.jpg"),
        "status": Term(r"available|pending|sold", "available"),
    }
    created_pet = {
        "id": Like(100),
        "name": Like("NewPet"),
        "photoUrls": EachLike("https://example.com/photo.jpg"),
        "status": Term(r"available|pending|sold", "available"),
    }

    (
        pact.given("the pet service is available")
        .upon_receiving("a POST request to create a pet")
        .with_request("POST", "/pet", headers={"Content-Type": "application/json"}, body=new_pet)
        .will_respond_with(200, body=created_pet)
    )

    import requests
    with pact:
        response = requests.post(
            f"http://{PACT_HOST}:{PACT_PORT}/pet",
            json={
                "name": "NewPet",
                "photoUrls": ["https://example.com/photo.jpg"],
                "status": "available",
            },
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        assert body["name"] == "NewPet"
