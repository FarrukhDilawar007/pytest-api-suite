import pytest
from src.models.user import User


@pytest.mark.smoke
@pytest.mark.regression
def test_create_user(user_client, unique_id):
    payload = {
        "id": unique_id,
        "username": f"testuser_{unique_id}",
        "firstName": "Jane",
        "lastName": "Doe",
        "email": f"jane_{unique_id}@example.com",
        "password": "Password123",
        "phone": "5550001111",
        "userStatus": 1,
    }
    response = user_client.create_user(payload)
    assert response.status_code == 200

    user_client.delete_user(payload["username"], raise_on_error=False)


@pytest.mark.smoke
@pytest.mark.regression
def test_get_user_by_username(user_client, unique_user):
    response = user_client.get_user(unique_user["username"])
    assert response.status_code == 200

    user = User.model_validate(response.json())
    assert user.username == unique_user["username"]
    assert user.email == unique_user["email"]


@pytest.mark.regression
def test_update_user(user_client, unique_user):
    updated_payload = {**unique_user, "firstName": "Updated"}
    response = user_client.update_user(unique_user["username"], updated_payload)
    assert response.status_code == 200


@pytest.mark.regression
def test_delete_user(user_client, unique_id):
    username = f"delete_me_{unique_id}"
    payload = {
        "id": unique_id,
        "username": username,
        "firstName": "Delete",
        "lastName": "Me",
        "email": f"delete_{unique_id}@example.com",
        "password": "Password123",
        "phone": "5550001111",
        "userStatus": 1,
    }
    user_client.create_user(payload)
    response = user_client.delete_user(username)
    assert response.status_code == 200


@pytest.mark.regression
def test_get_nonexistent_user_returns_404(user_client):
    response = user_client.get_user("no_such_user_xyz_99999", raise_on_error=False)
    assert response.status_code == 404


@pytest.mark.regression
def test_delete_nonexistent_user_returns_404(user_client):
    response = user_client.delete_user("no_such_user_xyz_99999", raise_on_error=False)
    assert response.status_code == 404
