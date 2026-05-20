import pytest
from src.models.pet import Pet


@pytest.mark.regression
@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_returns_list(pet_client, status):
    pets = pet_client.find_by_status(status)

    assert isinstance(pets, list)
    for pet in pets:
        assert isinstance(pet, Pet)
        # The public demo API has corrupted entries; only assert status on records that have it.
        if pet.status is not None:
            assert pet.status == status


@pytest.mark.regression
def test_find_by_status_all_statuses(pet_client):
    pets = pet_client.find_by_status(["available", "pending", "sold"])

    assert isinstance(pets, list)
    known_statuses = {"available", "pending", "sold", None}
    for pet in pets:
        assert pet.status in known_statuses


@pytest.mark.regression
def test_find_by_invalid_status(pet_client):
    response = pet_client.find_by_status_raw("nonexistent_status")
    assert response.status_code in (200, 400)
    if response.status_code == 200:
        assert response.json() == []
