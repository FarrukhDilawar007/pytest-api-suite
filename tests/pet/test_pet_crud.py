import pytest
from src.models.pet import Pet


@pytest.mark.smoke
@pytest.mark.regression
def test_create_pet(pet_client, unique_id):
    payload = {
        "id": unique_id,
        "name": f"TestPet_{unique_id}",
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available",
        "category": {"id": 1, "name": "dogs"},
        "tags": [{"id": 1, "name": "test"}],
    }
    pet = pet_client.create_pet(payload)

    assert isinstance(pet, Pet)
    assert pet.id == unique_id
    assert pet.name == f"TestPet_{unique_id}"
    assert pet.status == "available"

    pet_client.delete_pet(pet.id, raise_on_error=False)


@pytest.mark.smoke
@pytest.mark.regression
def test_get_pet_by_id(pet_client, unique_pet):
    response = pet_client.get_pet(unique_pet.id)
    pet = Pet.model_validate(response.json())

    assert pet.id == unique_pet.id
    assert pet.name == unique_pet.name


@pytest.mark.regression
def test_update_pet(pet_client, unique_pet):
    updated_payload = {
        "id": unique_pet.id,
        "name": f"{unique_pet.name}_updated",
        "photoUrls": unique_pet.photoUrls,
        "status": "pending",
    }
    updated = pet_client.update_pet(updated_payload)

    assert updated.id == unique_pet.id
    assert updated.status == "pending"
    assert "_updated" in updated.name


@pytest.mark.regression
def test_update_pet_with_form(pet_client, unique_pet):
    response = pet_client.update_pet_with_form(unique_pet.id, name="FormUpdated", status="sold")
    assert response.status_code in (200, 405)


@pytest.mark.smoke
@pytest.mark.regression
def test_delete_pet(pet_client, unique_id):
    payload = {
        "id": unique_id,
        "name": f"DeleteMe_{unique_id}",
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available",
    }
    pet = pet_client.create_pet(payload)
    response = pet_client.delete_pet(pet.id)
    assert response.status_code == 200


@pytest.mark.regression
def test_get_nonexistent_pet_returns_404(pet_client):
    response = pet_client.get_pet(999999999, raise_on_error=False)
    assert response.status_code == 404


@pytest.mark.regression
def test_get_pet_invalid_id_returns_400(pet_client):
    response = pet_client.get_pet("invalid-id", raise_on_error=False)
    assert response.status_code in (400, 404)


@pytest.mark.regression
def test_delete_already_deleted_pet(pet_client, unique_id):
    payload = {
        "id": unique_id,
        "name": f"TempPet_{unique_id}",
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available",
    }
    pet = pet_client.create_pet(payload)
    pet_client.delete_pet(pet.id)
    response = pet_client.delete_pet(pet.id, raise_on_error=False)
    assert response.status_code in (200, 404)
