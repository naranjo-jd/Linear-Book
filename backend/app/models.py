"""Database models for problems and submissions."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime

class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    section = Column(String, index=True)  # e.g., "section1", "taller1"
    problem_id = Column(String, unique=True, index=True)  # e.g., "VF1", "ex2.1"
    title = Column(String)
    description = Column(Text)
    problem_type = Column(String)  # code, math, multiple_choice, simulation
    
    # Problem configuration (stored as JSON in real implementation)
    expected_output = Column(Text, nullable=True)  # for code problems
    correct_answer = Column(Text, nullable=True)  # for math problems
    tolerance = Column(Float, default=0.01)  # for numerical answers
    
    # Multiple choice options (stored as JSON)
    options = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(String, index=True)
    user_id = Column(String, index=True, nullable=True)  # Optional for anonymous submissions
    
    submission_type = Column(String)  # code, math, multiple_choice, etc.
    submitted_answer = Column(Text)
    is_correct = Column(Boolean, nullable=True)
    feedback = Column(Text)
    
    # For code submissions
    execution_output = Column(Text, nullable=True)
    execution_error = Column(Text, nullable=True)
    
    # Grading details
    score = Column(Float, nullable=True)
    time_ms = Column(Float, nullable=True)  # execution time
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
