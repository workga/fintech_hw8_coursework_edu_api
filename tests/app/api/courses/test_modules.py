from tests.app.api.conftest import (
    add_teacher_model,
    add_student_model,
    get_course_create_schema,
    get_module_create_schema,
)

from app.crud.crud_user import crud_user


async def test_create_success(client, set_auth):
    db_teacher = await add_teacher_model()
    course_create = get_course_create_schema()

    set_auth(db_teacher)
    course = client.post(
        '/api/courses',
        json=course_create
    ).json()
    
    module_create = get_module_create_schema()
    response = client.post(
        f'/api/courses/{course["id"]}/modules',
        json=module_create
    )

    assert response.status_code == 201

    module = response.json()
    assert module["title"] == module_create["title"]
    assert module["theory"] == module_create["theory"]
    assert module["task"] == module_create["task"]
    assert module["duration"] == module_create["duration"]
    assert module["status"] == 'waiting'


async def test_create_fail_not_author(client, set_auth):
    db_teacher_1 = await add_teacher_model(1)
    course_create = get_course_create_schema()

    set_auth(db_teacher_1)
    course = client.post(
        '/api/courses',
        json=course_create
    ).json()
    
    db_teacher_2 = await add_teacher_model(2)
    set_auth(db_teacher_2)
    module_create = get_module_create_schema()
    response = client.post(
        f'/api/courses/{course["id"]}/modules',
        json=module_create
    )

    assert response.status_code == 403


async def test_get_list_success(client, set_auth):
    db_teacher = await add_teacher_model()
    course_create = get_course_create_schema()

    set_auth(db_teacher)
    course = client.post(
        '/api/courses',
        json=course_create
    ).json()
    
    for i in range(1, 4):
        client.post(
        f'/api/courses/{course["id"]}/modules',
        json=get_module_create_schema(i)
    )

    set_auth(None)
    response = client.get(
        f'/api/courses/{course["id"]}/modules'
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_info_for_teacher(client, set_auth, add_teacher_course_module):
    db_teacher, course, module = add_teacher_course_module

    set_auth(db_teacher)
    response = client.get(
        f'/api/courses/{course["id"]}/modules/{module["number"]}'
    )

    assert response.status_code == 200

    module_info = response.json()
    assert "theory" in module_info.keys()
    assert "task" in module_info.keys()


async def test_get_info_for_student(client, set_auth, add_teacher_course_module):
    _, course, module = add_teacher_course_module
    db_student = await add_student_model()

    set_auth(db_student)
    response = client.post(
        '/api/profile/courses',
        json={
            "course_id": course["id"]
        }
    )

    # Need to reload mocked auth, because user's relationships were not updated
    db_student = await crud_user.get_by_id(db_student.id)
    set_auth(db_student)
    response = client.get(
        f'/api/courses/{course["id"]}/modules/{module["number"]}'
    )

    assert response.status_code == 200

    module_info = response.json()
    assert module_info["theory"] == None
    assert module_info["task"] == None


async def test_get_info_for_student_forbidden(client, set_auth, add_teacher_course_module):
    _, course, module = add_teacher_course_module
    db_student = await add_student_model()

    set_auth(db_student)
    response = client.get(
        f'/api/courses/{course["id"]}/modules/{module["number"]}'
    )

    assert response.status_code == 403


async def test_get_info_too_big_number(client, set_auth, add_teacher_course_module):
    db_teacher, course, module = add_teacher_course_module

    set_auth(db_teacher)
    response = client.get(
        f'/api/courses/{course["id"]}/modules/{module["number"] + 1}'
    )

    assert response.status_code == 404