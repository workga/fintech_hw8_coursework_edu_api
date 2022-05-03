import pytest

from app.crud.crud_user import crud_user
from tests.app.api.conftest import add_teacher_model, get_teacher_create_schema


@pytest.mark.parametrize('role', ['student', 'teacher', 'admin'])
def test_create_user(client, set_auth, role):
    db_admin = crud_user.get_by_email('admin@api.edu')
    teacher_create = get_teacher_create_schema()
    teacher_create['role'] = role

    set_auth(db_admin)
    response = client.post('/api/admin/users', json=teacher_create)

    assert response.status_code == 201

    teacher = response.json()
    assert teacher['first_name'] == teacher_create['first_name']
    assert teacher['last_name'] == teacher_create['last_name']
    assert teacher['role'] == role


async def test_create_user_fail_email_exists(client, set_auth):
    db_admin = crud_user.get_by_email('admin@api.edu')
    await add_teacher_model(1)

    set_auth(db_admin)
    response = client.post('/api/admin/users', json=get_teacher_create_schema())

    assert response.status_code == 400
