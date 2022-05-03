import pytest

from tests.app.api.conftest import add_student_model, add_teacher_model, get_student_create_schema


async def test_success(client):
    db_user = await add_student_model(n=1)

    response = client.post(
        '/api/auth/login',
        json={
            "email": db_user.email,
            "password": "student_1"
        }
    )

    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token.keys()
    assert "refresh_token" in token.keys()


async def test_fail_wrong_email(client):
    await add_student_model(n=1)

    response = client.post(
        '/api/auth/login',
        json={
            "email": "wrong_email@api.edu",
            "password": "student_1"
        }
    )

    assert response.status_code == 401


async def test_fail_wrong_password(client):
    db_user = await add_student_model(n=1)

    response = client.post(
        '/api/auth/login',
        json={
            "email": db_user.email,
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401
    