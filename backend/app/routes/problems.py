"""Route handlers for problem management."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Problem
from app.schemas import Problem as ProblemSchema, ProblemCreate

router = APIRouter()

@router.get("/problems/{problem_id}", response_model=ProblemSchema)
async def get_problem(problem_id: str, db: Session = Depends(get_db)):
    """Get problem details by problem_id."""
    problem = db.query(Problem).filter(Problem.problem_id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.get("/problems/section/{section}", response_model=list[ProblemSchema])
async def get_section_problems(section: str, db: Session = Depends(get_db)):
    """Get all problems in a section."""
    problems = db.query(Problem).filter(Problem.section == section).all()
    return problems

@router.post("/problems", response_model=ProblemSchema)
async def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    """Create a new problem."""
    db_problem = Problem(**problem.model_dump())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem
