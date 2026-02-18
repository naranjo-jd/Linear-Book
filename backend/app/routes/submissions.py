"""Route handlers for problem submissions and grading."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from app.db import get_db
from app.models import Submission, Problem
from app.schemas import (
    CodeSubmission, 
    MathSubmission, 
    MultipleChoiceSubmission,
    SubmissionResponse
)
from app.services.grader import grade_code_submission, grade_math_submission

router = APIRouter()

@router.post("/submit/code", response_model=SubmissionResponse)
async def submit_code(submission: CodeSubmission, db: Session = Depends(get_db)):
    """Submit code solution for a problem."""
    problem = db.query(Problem).filter(Problem.problem_id == submission.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    if problem.problem_type != "code":
        raise HTTPException(status_code=400, detail="This problem is not a code problem")
    
    # Grade the submission
    start_time = time.time()
    is_correct, feedback, output, error = grade_code_submission(
        submission.code,
        problem.expected_output
    )
    elapsed_ms = (time.time() - start_time) * 1000
    
    # Save submission to database
    db_submission = Submission(
        problem_id=submission.problem_id,
        user_id=submission.user_id,
        submission_type="code",
        submitted_answer=submission.code,
        is_correct=is_correct,
        feedback=feedback,
        execution_output=output,
        execution_error=error,
        score=1.0 if is_correct else 0.0,
        time_ms=elapsed_ms
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return {
        "submission_id": db_submission.id,
        "problem_id": submission.problem_id,
        "is_correct": is_correct,
        "feedback": feedback,
        "score": db_submission.score,
        "execution_output": output,
        "execution_error": error
    }

@router.post("/submit/math", response_model=SubmissionResponse)
async def submit_math(submission: MathSubmission, db: Session = Depends(get_db)):
    """Submit mathematical answer for a problem."""
    problem = db.query(Problem).filter(Problem.problem_id == submission.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    if problem.problem_type != "math":
        raise HTTPException(status_code=400, detail="This problem is not a math problem")
    
    # Grade the submission
    is_correct, feedback = grade_math_submission(
        submission.answer,
        problem.correct_answer,
        problem.tolerance
    )
    
    # Save submission to database
    db_submission = Submission(
        problem_id=submission.problem_id,
        user_id=submission.user_id,
        submission_type="math",
        submitted_answer=submission.answer,
        is_correct=is_correct,
        feedback=feedback,
        score=1.0 if is_correct else 0.0
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return {
        "submission_id": db_submission.id,
        "problem_id": submission.problem_id,
        "is_correct": is_correct,
        "feedback": feedback,
        "score": db_submission.score
    }

@router.post("/submit/multiple-choice", response_model=SubmissionResponse)
async def submit_multiple_choice(
    submission: MultipleChoiceSubmission, 
    db: Session = Depends(get_db)
):
    """Submit multiple choice answer for a problem."""
    problem = db.query(Problem).filter(Problem.problem_id == submission.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    if problem.problem_type != "multiple_choice":
        raise HTTPException(status_code=400, detail="This problem is not a multiple choice problem")
    
    # For now, assume correct_answer stores the index of correct option
    try:
        correct_option = int(problem.correct_answer)
        is_correct = submission.selected_option == correct_option
    except:
        is_correct = False
    
    feedback = problem.explanation if is_correct else "Incorrect. " + (problem.explanation or "")
    
    db_submission = Submission(
        problem_id=submission.problem_id,
        user_id=submission.user_id,
        submission_type="multiple_choice",
        submitted_answer=str(submission.selected_option),
        is_correct=is_correct,
        feedback=feedback,
        score=1.0 if is_correct else 0.0
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return {
        "submission_id": db_submission.id,
        "problem_id": submission.problem_id,
        "is_correct": is_correct,
        "feedback": feedback,
        "score": db_submission.score
    }
