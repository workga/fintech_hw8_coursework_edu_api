import pytest

from app.crud.crud_module import crud_module
from tests.app.api.conftest import add_student_model


async def test_publish_solution(client, set_auth, add_student_enroll_course):
    _, course, module, db_student = add_student_enroll_course
    await crud_module.set_status(module['id'], 'started')

    # Do it twice to check that user can update his solution
    set_auth(db_student)
    for i in range(2):
        response = client.put(
            'api/profile/solutions',
            json={
                'course_id': course['id'],
                'module_number': module['number'],
                'text': f'text_{i}',
            },
        )

        assert response.status_code == 200
        solution = response.json()

        assert solution['teacher_id'] is None
        assert solution['review'] is None
        assert solution['score'] is None
        assert solution['text'] == f'text_{i}'
        assert solution['course_id'] == course['id']
        assert solution['module_number'] == module['number']
        assert solution['student_id'] == db_student.id
        assert solution['status'] == 'waiting'


async def test_publish_solution_fail_module_not_found(
    client, set_auth, add_student_enroll_course
):
    _, course, module, db_student = add_student_enroll_course
    await crud_module.set_status(module['id'], 'started')

    set_auth(db_student)
    response = client.put(
        'api/profile/solutions',
        json={
            'course_id': course['id'],
            'module_number': module['number'] + 1,
            'text': 'text',
        },
    )

    assert response.status_code == 400


@pytest.mark.parametrize('status', ['waiting', 'finished'])
async def test_publish_solution_fail_module_status(
    client, set_auth, add_student_enroll_course, status
):
    _, course, module, db_student = add_student_enroll_course
    await crud_module.set_status(module['id'], status)

    set_auth(db_student)
    response = client.put(
        'api/profile/solutions',
        json={
            'course_id': course['id'],
            'module_number': module['number'],
            'text': 'text',
        },
    )

    assert response.status_code == 400


async def test_publish_solution_fail_forbidden(
    client, set_auth, add_teacher_course_module
):
    _, course, module = add_teacher_course_module
    db_student = await add_student_model()

    await crud_module.set_status(module['id'], 'started')

    set_auth(db_student)
    response = client.put(
        'api/profile/solutions',
        json={
            'course_id': course['id'],
            'module_number': module['number'],
            'text': 'text',
        },
    )

    assert response.status_code == 403


def test_list_solutions_student(client, set_auth, add_solution):
    *_, db_student, _ = add_solution

    set_auth(db_student)
    response = client.get('api/profile/solutions')

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_list_solutions_teacher(client, set_auth, add_solution):
    db_teacher, *_ = add_solution

    set_auth(db_teacher)
    response = client.get('api/profile/solutions')

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_info_solution_student(client, set_auth, add_solution):
    db_teacher, *_, db_student, solution = add_solution

    set_auth(db_student)
    response = client.get(f'api/profile/solutions/{solution["id"]}')

    assert response.status_code == 200

    solution_info = response.json()
    assert solution_info['text'] == 'text'
    assert solution_info['student_id'] == db_student.id
    assert solution_info['teacher_id'] == db_teacher.id
    assert solution_info['review'] is None
    assert solution_info['score'] is None


async def test_info_solution_teacher(client, set_auth, add_solution):
    db_teacher, *_, db_student, solution = add_solution

    set_auth(db_teacher)
    response = client.get(f'api/profile/solutions/{solution["id"]}')

    assert response.status_code == 200

    solution_info = response.json()
    assert solution_info['text'] == 'text'
    assert solution_info['student_id'] == db_student.id
    assert solution_info['teacher_id'] == db_teacher.id
    assert solution_info['review'] is None
    assert solution_info['score'] is None


async def test_info_solution_fail_not_found(client, set_auth, add_solution):
    db_teacher, *_, solution = add_solution

    set_auth(db_teacher)
    response = client.get(f'api/profile/solutions/{solution["id"] + 1}')

    assert response.status_code == 404


def test_publish_review_success(client, set_auth, add_solution):
    db_teacher, *_, solution = add_solution

    set_auth(db_teacher)
    response = client.put(
        f'api/profile/solutions/{solution["id"]}',
        json={'review': 'review', 'score': 10},
    )

    assert response.status_code == 200

    solution_info = response.json()
    assert solution_info['review'] == 'review'
    assert solution_info['score'] == 10
    assert solution_info['status'] == 'reviewed'


def test_publish_review_not_found(client, set_auth, add_solution):
    db_teacher, *_, solution = add_solution

    set_auth(db_teacher)
    response = client.put(
        f'api/profile/solutions/{solution["id"] + 1}',
        json={'review': 'review', 'score': 10},
    )

    assert response.status_code == 404
