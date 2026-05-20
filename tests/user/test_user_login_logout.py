import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_login_valid_user(user_client, unique_user):
    response = user_client.login(unique_user["username"], unique_user["password"])

    assert response.status_code == 200
    assert "X-Rate-Limit" in response.headers or "X-Expires-After" in response.headers or response.text


@pytest.mark.regression
def test_login_invalid_credentials(user_client):
    # The PetStore demo API returns 200 for bad credentials (no real auth enforcement).
    # Assert the call completes and is not a 5xx server error.
    response = user_client.login("nonexistent_user_xyz_$$", "wrongpassword", raise_on_error=False)
    assert response.status_code in (200, 400), (
        f"Unexpected status {response.status_code}: {response.text}"
    )


@pytest.mark.regression
def test_logout(user_client):
    response = user_client.logout()
    assert response.status_code == 200
