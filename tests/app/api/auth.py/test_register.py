import pytest

from tests.app.api.conftest import add_student_model, get_student_create_schema


def test_success(client):
    user_create = get_student_create_schema()

    response = client.post(
        '/api/auth/register',
        json=user_create
    )

    assert response.status_code == 201
    user = response.json()
    assert user["first_name"] == user_create["first_name"]
    assert user["last_name"] == user_create["last_name"]
    assert user["role"] == "student"


@pytest.mark.parametrize(
    'role', [
    'teacher',
    'admin',
])
def test_fail_wrong_role(client, role):
    user_create = get_student_create_schema()

    user_create["role"] = role

    response = client.post(
        '/api/auth/register',
        json=user_create
    )

    assert response.status_code == 403


async def test_fail_email_registered(client):
    db_user = await add_student_model(1)
    user_create = get_student_create_schema(2)

    user_create["email"] = db_user.email

    response = client.post(
        '/api/auth/register',
        json=user_create
    )
    
    assert response.status_code == 400