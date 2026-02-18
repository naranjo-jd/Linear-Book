"""Grading logic for different problem types."""

import subprocess
import re
from typing import Tuple
import numpy as np
from app.config import settings

def grade_code_submission(code: str, expected_output: str) -> Tuple[bool, str, str, str]:
    """
    Grade a code submission by executing it and comparing output.
    
    Returns: (is_correct, feedback, output, error)
    """
    if len(code) > settings.MAX_CODE_LENGTH:
        return False, "Code is too long", "", "Code exceeds maximum length"
    
    try:
        # Execute code in subprocess with timeout
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=settings.SANDBOX_TIMEOUT
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if result.returncode != 0:
            return False, "Code execution failed", output, error
        
        # Compare output (simple string comparison for now)
        is_correct = output == expected_output.strip()
        
        feedback = "Correct!" if is_correct else f"Expected:\n{expected_output}\n\nGot:\n{output}"
        
        return is_correct, feedback, output, error
        
    except subprocess.TimeoutExpired:
        return False, "Code execution timed out", "", "Execution exceeded time limit"
    except Exception as e:
        return False, "Error executing code", "", str(e)

def grade_math_submission(answer: str, correct_answer: str, tolerance: float = 0.01) -> Tuple[bool, str]:
    """
    Grade a mathematical answer submission.
    
    Handles:
    - Numerical answers (with tolerance)
    - Simple LaTeX expressions (basic support)
    
    Returns: (is_correct, feedback)
    """
    try:
        # Try to parse as float
        student_val = float(answer.replace(",", "."))
        correct_val = float(correct_answer.replace(",", "."))
        
        is_correct = abs(student_val - correct_val) <= tolerance
        
        feedback = "Correct!" if is_correct else f"Expected: {correct_answer}, Got: {answer}"
        return is_correct, feedback
        
    except ValueError:
        # Handle non-numeric answers (basic string comparison)
        answer_clean = answer.strip().lower()
        correct_clean = correct_answer.strip().lower()
        
        is_correct = answer_clean == correct_clean
        feedback = "Correct!" if is_correct else f"Expected: {correct_answer}, Got: {answer}"
        return is_correct, feedback
