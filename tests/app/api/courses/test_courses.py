from tests.app.api.conftest import add_teacher_model, add_student_model, get_course_create_schema


async def test_create_success(client, set_auth):
    db_teacher = await add_teacher_model()
    course_create = get_course_create_schema()
    
    set_auth(db_teacher)
    response = client.post(
        '/api/courses',
        json=course_create
    )

    assert response.status_code == 201

    course = response.json()
    assert course["author_id"] == db_teacher.id
    assert course["title"] == course_create["title"]
    assert course["info"] == course_create["info"]
    assert course["start"] == course_create["start"]
    assert course["duration"] == course_create["duration"]
    assert course["status"] == 'waiting'


async def test_get_list_success(client, set_auth):
    db_teacher = await add_teacher_model()

    set_auth(db_teacher)
    for i in range(1, 4):
        client.post(
            '/api/courses',
            json=get_course_create_schema(i)
        )
    
    set_auth(None)
    response = client.get(
        '/api/courses'
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_info_success(client, set_auth):
    db_teacher = await add_teacher_model()
    course_create = get_course_create_schema()

    set_auth(db_teacher)
    client.post(
        '/api/courses',
        json=course_create
    )

    set_auth(None)
    response = client.get(
        '/api/courses/1'
    )

    assert response.status_code == 200
    course = response.json()

    assert course["author_id"] == db_teacher.id
    assert course["title"] == course_create["title"]
    assert course["info"] == course_create["info"]
    assert course["start"] == course_create["start"]
    assert course["duration"] == course_create["duration"]
    assert course["status"] == 'waiting'
