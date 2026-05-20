import pytest


@pytest.mark.regression
def test_create_users_with_list(user_client, unique_id):
    users = [
        {
            "id": unique_id + 10,
            "username": f"list_user_a_{unique_id}",
            "firstName": "Charlie",
            "lastName": "List",
            "email": f"charlie_{unique_id}@example.com",
            "password": "Password123",
            "phone": "5550003333",
            "userStatus": 1,
        },
        {
            "id": unique_id + 11,
            "username": f"list_user_b_{unique_id}",
            "firstName": "Diana",
            "lastName": "List",
            "email": f"diana_{unique_id}@example.com",
            "password": "Password123",
            "phone": "5550004444",
            "userStatus": 1,
        },
    ]
    response = user_client.create_with_list(users)
    assert response.status_code == 200

    for user in users:
        user_client.delete_user(user["username"], raise_on_error=False)
