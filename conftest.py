import random
import pytest
from src.clients.pet_client import PetClient
from src.clients.store_client import StoreClient
from src.clients.user_client import UserClient

BASE_URL = "https://petstore.swagger.io/v2"
API_KEY = "special-key"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_key():
    return API_KEY


@pytest.fixture(scope="session")
def pet_client(base_url, api_key):
    return PetClient(base_url, api_key)


@pytest.fixture(scope="session")
def store_client(base_url, api_key):
    return StoreClient(base_url, api_key)


@pytest.fixture(scope="session")
def user_client(base_url, api_key):
    return UserClient(base_url, api_key)


@pytest.fixture
def unique_id():
    return random.randint(1_000_000, 9_999_999)


@pytest.fixture
def unique_pet(pet_client, unique_id):
    payload = {
        "id": unique_id,
        "name": f"TestPet_{unique_id}",
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available",
        "category": {"id": 1, "name": "dogs"},
        "tags": [{"id": 1, "name": "test"}],
    }
    pet = pet_client.create_pet(payload)
    yield pet
    pet_client.delete_pet(pet.id, raise_on_error=False)


@pytest.fixture
def unique_user(user_client, unique_id):
    payload = {
        "id": unique_id,
        "username": f"testuser_{unique_id}",
        "firstName": "Test",
        "lastName": "User",
        "email": f"test_{unique_id}@example.com",
        "password": "Password123",
        "phone": "5550001111",
        "userStatus": 1,
    }
    user_client.create_user(payload)
    yield payload
    user_client.delete_user(payload["username"], raise_on_error=False)
