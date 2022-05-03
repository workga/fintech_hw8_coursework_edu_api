from typing import Optional

from sqlalchemy import select

from app.crud.crud_base import CRUDBase
from app.crud.crud_user import crud_user
from app.database.db import create_session
from app.models.solution import Solution
from app.schemas.solution import SolutionPut, SolutionReviewPut


class CRUDSolution(CRUDBase[Solution]):
    async def set_teacher(
        self, solution_id: int, teacher_id: int
    ) -> Optional[Solution]:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(Solution).where(Solution.id == solution_id)
                )
            ).one_or_none()

            solution = self.row_to_model(row)
            if solution is None:
                return None

            if await crud_user.get_by_id(teacher_id) is None:
                return None

            solution.teacher_id = teacher_id
            await session.flush()
            await session.refresh(solution)

        return solution

    async def put(self, solution_put: SolutionPut, student_id: int) -> Solution:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(Solution)
                    .where(Solution.course_id == solution_put.course_id)
                    .where(Solution.module_number == solution_put.module_number)
                    .where(Solution.student_id == student_id)
                )
            ).one_or_none()

            solution = self.row_to_model(row)
            if solution:
                solution.text = solution_put.text
                await session.flush()
                await session.refresh(solution)
            else:
                solution = await super().create(solution_put, student_id=student_id)

        return solution

    async def put_review(
        self,
        review_put: SolutionReviewPut,
        solution_id: int,
    ) -> Solution:
        async with create_session() as session:
            row = (
                await session.execute(
                    select(Solution).where(Solution.id == solution_id)
                )
            ).one()

            solution = self.row_to_model(row)

            solution.review = review_put.review
            solution.score = review_put.score
            solution.status = 'reviewed'
            await session.flush()
            await session.refresh(solution)

        return solution


crud_solution = CRUDSolution(Solution)
