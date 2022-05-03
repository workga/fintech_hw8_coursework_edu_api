import pytest

from app.core.security import hash_password
from app.crud.crud_module import crud_module
from app.crud.crud_solution import crud_solution
from app.crud.crud_user import crud_user
from app.database.db import create_session
from app.models.user import User


async def add_model(model):
    async with create_session() as session:
        db_model = model
        session.add(db_model)
        await session.flush()
        await session.refresh(db_model)

    return db_model


async def add_student_model(n: int = 1):
    student = User(
        email=f'student_{n}@api.edu',
        password=hash_password(f'student_{n}'),
        first_name=f'Student_{n}',
        last_name=f'S_{n}.',
        role='student',
    )
    return await add_model(student)


async def add_teacher_model(n: int = 1):
    teacher = User(
        email=f'teacher_{n}@api.edu',
        password=hash_password(f'teacher_{n}'),
        first_name=f'Teacher_{n}',
        last_name=f'T_{n}.',
        role='teacher',
    )
    return await add_model(teacher)


def get_student_create_schema(n: int = 1):
    return {
        'email': f'student_{n}@api.edu',
        'password': f'student_{n}',
        'first_name': f'Student_{n}',
        'last_name': f'S_{n}.',
        'role': 'student',
    }


def get_teacher_create_schema(n: int = 1):
    return {
        'email': f'teacher_{n}@api.edu',
        'password': f'teacher_{n}',
        'first_name': f'Teacher_{n}',
        'last_name': f'T_{n}.',
        'role': 'teacher',
    }


def get_course_create_schema(n: int = 1):
    return {
        'title': f'Course_{n}: Title',
        'info': f'Course_{n}: Info',
        'start': '2022-06-01',
        'duration': 28,
    }


def get_module_create_schema(n: int = 1):
    return {
        'title': f'Module_{n}: Title',
        'theory': f'Module_{n}: Theory',
        'task': f'Module_{n}: Task',
        'duration': 7,
    }


@pytest.fixture(name='add_teacher_course_module')
async def fixture_add_teacher_course_module(client, set_auth):
    db_teacher = await add_teacher_model()
    course_create = get_course_create_schema()

    set_auth(db_teacher)
    course = client.post('/api/courses', json=course_create).json()

    module_create = get_module_create_schema()
    module = client.post(
        f'/api/courses/{course["id"]}/modules', json=module_create
    ).json()

    return db_teacher, course, module


@pytest.fixture(name='add_student_enroll_course')
async def fixture_add_student_enroll_course(
    client, set_auth, add_teacher_course_module
):
    db_teacher, course, module = add_teacher_course_module
    db_student = await add_student_model()

    set_auth(db_student)
    client.post('api/profile/courses', json={'course_id': course['id']})

    db_student = await crud_user.get_by_id(db_student.id)

    return db_teacher, course, module, db_student


@pytest.fixture(name='add_solution')
async def fixture_add_solution(client, set_auth, add_student_enroll_course):
    db_teacher, course, module, db_student = add_student_enroll_course

    await crud_module.set_status(module['id'], 'started')

    set_auth(db_student)
    solution = client.put(
        'api/profile/solutions',
        json={
            'course_id': course['id'],
            'module_number': module['number'],
            'text': 'text',
        },
    ).json()

    await crud_solution.set_teacher(solution['id'], db_teacher.id)

    db_teacher = await crud_user.get_by_id(db_teacher.id)
    db_student = await crud_user.get_by_id(db_student.id)
    return db_teacher, course, module, db_student, solution


@pytest.fixture(name='student_token')
async def fixture_student_token(client):
    db_student = await add_student_model(1)

    token = client.post(
        '/api/auth/login', json={'email': db_student.email, 'password': 'student_1'}
    ).json()

    return db_student, token
