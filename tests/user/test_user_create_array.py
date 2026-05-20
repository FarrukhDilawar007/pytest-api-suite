import pytest


@pytest.mark.regression
def test_create_users_with_array(user_client, unique_id):
    users = [
        {
            "id": unique_id,
            "username": f"array_user_a_{unique_id}",
            "firstName": "Alice",
            "lastName": "Array",
            "email": f"alice_{unique_id}@example.com",
            "password": "Password123",
            "phone": "5550001111",
            "userStatus": 1,
        },
        {
            "id": unique_id + 1,
            "username": f"array_user_b_{unique_id}",
            "firstName": "Bob",
            "lastName": "Array",
            "email": f"bob_{unique_id}@example.com",
            "password": "Password123",
            "phone": "5550002222",
            "userStatus": 1,
        },
    ]
    response = user_client.create_with_array(users)
    assert response.status_code == 200

    for user in users:
        user_client.delete_user(user["username"], raise_on_error=False)
