from app.crud.crud_user import crud_user
from tests.app.api.conftest import (
    add_student_model,
    add_teacher_model,
    get_course_create_schema,
)


async def test_list_courses(client, set_auth):
    db_teacher_author = await add_teacher_model()
    db_student = await add_student_model()
    db_teacher = await add_teacher_model(2)

    set_auth(db_teacher_author)
    for i in range(2):
        client.post('/api/courses', json=get_course_create_schema(i))

    for user in (db_student, db_teacher):
        set_auth(user)
        for i in range(2):
            client.post('api/profile/courses', json={'course_id': i + 1})

        # Need to reload mocked auth, because user's relationships were not updated
        user = await crud_user.get_by_id(user.id)
        set_auth(user)
        response = client.get(
            'api/profile/courses',
        )

        assert response.status_code == 200
        courses = response.json()
        assert len(courses) == 2


async def test_enroll_course(client, set_auth, add_teacher_course_module):
    _, course, _ = add_teacher_course_module
    db_student = await add_student_model()
    db_teacher = await add_teacher_model(2)

    for user in (db_student, db_teacher):
        set_auth(user)
        response = client.post('api/profile/courses', json={'course_id': course['id']})

        assert response.status_code == 201
        courses = response.json()
        assert len(courses) == 1


async def test_enroll_course_fail_already_enrolled(
    client, set_auth, add_teacher_course_module
):
    _, course, _ = add_teacher_course_module
    db_student = await add_student_model()

    set_auth(db_student)
    for _ in range(2):
        response = client.post('api/profile/courses', json={'course_id': course['id']})

    assert response.status_code == 400


async def test_enroll_course_fail_course_not_exist(
    client, set_auth, add_teacher_course_module
):
    _, course, _ = add_teacher_course_module
    db_student = await add_student_model()

    set_auth(db_student)
    response = client.post('api/profile/courses', json={'course_id': course['id'] + 1})

    assert response.status_code == 400
