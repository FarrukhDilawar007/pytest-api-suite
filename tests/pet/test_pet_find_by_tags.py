import pytest
from src.models.pet import Pet


@pytest.mark.regression
def test_find_by_single_tag(pet_client):
    pets = pet_client.find_by_tags(["test"])

    assert isinstance(pets, list)
    for pet in pets:
        assert isinstance(pet, Pet)


@pytest.mark.regression
def test_find_by_multiple_tags(pet_client):
    pets = pet_client.find_by_tags(["test", "string"])

    assert isinstance(pets, list)
    for pet in pets:
        assert isinstance(pet, Pet)
