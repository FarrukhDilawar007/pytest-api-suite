"""
Step definitions and fixtures for BDD scenarios.
Steps are collected automatically by pytest-bdd from conftest.py.
"""
import random
import pytest
from pytest_bdd import given, when, then, parsers
from src.models.pet import Pet


# ---------------------------------------------------------------------------
# Shared BDD state holder (one per test via fixture injection)
# ---------------------------------------------------------------------------

@pytest.fixture
def bdd_context():
    return {}


# ---------------------------------------------------------------------------
# Pet lifecycle steps
# ---------------------------------------------------------------------------

@given(parsers.parse('I have a pet payload with name "{name}" and status "{status}"'))
def pet_payload(bdd_context, name, status):
    uid = random.randint(1_000_000, 9_999_999)
    bdd_context["pet_payload"] = {
        "id": uid,
        "name": name,
        "photoUrls": ["https://example.com/bdd.jpg"],
        "status": status,
    }


@when("I send a POST request to create the pet")
def create_pet_request(bdd_context, pet_client):
    response = pet_client._request("POST", "/pet", json=bdd_context["pet_payload"], raise_on_error=False)
    bdd_context["response"] = response
    if response.status_code == 200:
        bdd_context["pet"] = Pet.model_validate(response.json())


@then(parsers.parse("the response status should be {code:d}"))
def assert_response_status(bdd_context, code):
    assert bdd_context["response"].status_code == code


@then(parsers.parse('the pet name should be "{name}"'))
def assert_pet_name(bdd_context, name):
    assert bdd_context["pet"].name == name


@then(parsers.parse('the pet status should be "{status}"'))
def assert_pet_status(bdd_context, status):
    assert bdd_context["pet"].status == status


@given("a pet exists in the store")
def existing_pet(bdd_context, pet_client):
    uid = random.randint(1_000_000, 9_999_999)
    payload = {
        "id": uid,
        "name": f"BDDExisting_{uid}",
        "photoUrls": ["https://example.com/bdd.jpg"],
        "status": "available",
    }
    pet = pet_client.create_pet(payload)
    bdd_context["pet"] = pet


@when(parsers.parse('I update the pet status to "{status}"'))
def update_pet_status(bdd_context, pet_client, status):
    pet = bdd_context["pet"]
    payload = {
        "id": pet.id,
        "name": pet.name,
        "photoUrls": pet.photoUrls,
        "status": status,
    }
    response = pet_client._request("PUT", "/pet", json=payload, raise_on_error=False)
    bdd_context["response"] = response
    if response.status_code == 200:
        bdd_context["pet"] = Pet.model_validate(response.json())


@when("I delete the pet")
def delete_pet_step(bdd_context, pet_client):
    pet = bdd_context["pet"]
    response = pet_client.delete_pet(pet.id, raise_on_error=False)
    bdd_context["response"] = response
    bdd_context["deleted_pet_id"] = pet.id


@then("the pet should no longer be found")
def assert_pet_not_found(bdd_context, pet_client):
    response = pet_client.get_pet(bdd_context["deleted_pet_id"], raise_on_error=False)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# User management steps
# ---------------------------------------------------------------------------

@given(parsers.parse('I have a user payload with username "{username}"'))
def user_payload(bdd_context, username):
    uid = random.randint(1_000_000, 9_999_999)
    bdd_context["user_payload"] = {
        "id": uid,
        "username": username,
        "firstName": "BDD",
        "lastName": "User",
        "email": f"{username}@example.com",
        "password": "Password123",
        "phone": "5550009999",
        "userStatus": 1,
    }


@when("I send a POST request to create the user")
def create_user_request(bdd_context, user_client):
    response = user_client.create_user(bdd_context["user_payload"])
    bdd_context["user_response"] = response


@then(parsers.parse("the user creation response status should be {code:d}"))
def assert_user_creation_status(bdd_context, code):
    assert bdd_context["user_response"].status_code == code


@then(parsers.parse('the user "{username}" should exist in the system'))
def assert_user_exists(bdd_context, user_client, username):
    response = user_client.get_user(username, raise_on_error=False)
    assert response.status_code == 200
    user_client.delete_user(username, raise_on_error=False)


@given(parsers.parse('a user "{username}" exists with password "{password}"'))
def create_login_user(bdd_context, user_client, username, password):
    uid = random.randint(1_000_000, 9_999_999)
    payload = {
        "id": uid,
        "username": username,
        "firstName": "BDD",
        "lastName": "Login",
        "email": f"{username}@example.com",
        "password": password,
        "phone": "5550009999",
        "userStatus": 1,
    }
    user_client.create_user(payload)
    bdd_context["login_user"] = payload


@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login_step(bdd_context, user_client, username, password):
    response = user_client.login(username, password, raise_on_error=False)
    bdd_context["login_response"] = response


@then(parsers.parse("the login response status should be {code:d}"))
def assert_login_status(bdd_context, code):
    assert bdd_context["login_response"].status_code == code


@then("the response should contain a session token")
def assert_session_token(bdd_context, user_client):
    response = bdd_context["login_response"]
    assert response.text or response.headers.get("X-Expires-After")
    user = bdd_context.get("login_user")
    if user:
        user_client.delete_user(user["username"], raise_on_error=False)
