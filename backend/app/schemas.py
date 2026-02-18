"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

# Problem schemas
class ProblemBase(BaseModel):
    title: str
    description: str
    problem_type: str  # code, math, multiple_choice, simulation
    section: str
    problem_id: str

class ProblemCreate(ProblemBase):
    expected_output: Optional[str] = None
    correct_answer: Optional[str] = None
    tolerance: float = 0.01
    options: Optional[str] = None
    explanation: Optional[str] = None

class Problem(ProblemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Submission schemas
class CodeSubmission(BaseModel):
    problem_id: str
    code: str
    user_id: Optional[str] = None

class MathSubmission(BaseModel):
    problem_id: str
    answer: str  # Could be number or LaTeX
    user_id: Optional[str] = None

class MultipleChoiceSubmission(BaseModel):
    problem_id: str
    selected_option: int
    user_id: Optional[str] = None

class SubmissionResponse(BaseModel):
    submission_id: int
    problem_id: str
    is_correct: bool
    feedback: str
    score: Optional[float] = None
    execution_output: Optional[str] = None
    execution_error: Optional[str] = None

# Health check
class HealthResponse(BaseModel):
    status: str
    version: str
