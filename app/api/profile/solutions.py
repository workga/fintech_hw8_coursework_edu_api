from typing import List
from fastapi import APIRouter, Depends, Body, HTTPException, status, Path

from app.api.deps import Auth
from app.crud.crud_module import crud_module
from app.crud.crud_solution import crud_solution
from app.models.solution import Solution
from app.schemas.solution import SolutionInfo, SolutionPut, SolutionRead, SolutionReviewPut

router = APIRouter()


@router.get(
    '',
    response_model=List[SolutionRead]
)
async def list_solutions(
    auth: Auth = Depends()
):
    user = await auth.check_roles(['student', 'teacher'])

    if user.role == 'student':
        solutions = user.sent_solutions
    else:
        solutions = user.received_solutions

    return solutions


@router.put(
    '',
    response_model=SolutionInfo
)
async def publish_solution(
    solution_put: SolutionPut = Body(...),
    auth: Auth = Depends()
):
    user = await auth.check_roles(['student'])

    module = await crud_module.get_by_number_in_course(
        course_id=solution_put.course_id,
        number=solution_put.module_number
    )
    if module is None or module.status != 'started':
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    if module.course_id not in [owned_course.id for owned_course in user.students_courses]:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    solution = await crud_solution.put(solution_put, student_id=user.id)

    return solution


@router.get(
    '/{solution_id}',
    response_model=SolutionInfo
)
async def info_solution(
    # Something like 'solution_exists' dependency is not used,
    # because unregistered user must not know whether solution exists or not
    solution_id: int = Path(..., ge=1), 
    auth: Auth = Depends(),
) -> Solution:
    user = await auth.check_roles(['student', 'teacher'])
    
    if user.role == 'student':
        solutions = user.sent_solutions
    else:
        solutions = user.received_solutions

    for solution in solutions:
        if solution.id == solution_id:
            return solution
    
    raise HTTPException(status.HTTP_404_NOT_FOUND)

    
@router.put(
    '/{solution_id}',
    response_model=SolutionInfo
)
async def publish_review(
    solution_id: int = Path(..., ge=1),
    review_put: SolutionReviewPut = Body(...),
    auth: Auth = Depends()
):
    user = await auth.check_roles(['teacher'])

    for solution in user.received_solutions:
        if solution.id == solution_id:
            return await crud_solution.put_review(
                review_put,
                solution_id=solution.id,
            )

    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.get('/{solution_id}/messages')
async def list_messages():
    pass


@router.post('/{solution_id}/messages')
async def send_message():
    pass