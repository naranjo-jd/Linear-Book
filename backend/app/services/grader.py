"""Lógica de calificación para los distintos tipos de problemas."""

import subprocess
import re
from typing import Tuple
from app.config import settings


def _normalize_numeric(value: str) -> str:
    """
    Intenta representar un string numérico de forma canónica.
    '6.0' → '6', '-2.0' → '-2', '3.14159' → '3.14159'
    Si no es numérico, retorna el string original.
    """
    try:
        f = float(value.strip())
        if f == int(f):
            return str(int(f))
        return str(f)
    except (ValueError, OverflowError):
        return value.strip()


def grade_code_submission(code: str, expected_output: str) -> Tuple[bool, str, str, str]:
    """
    Califica una solución de código ejecutándola y comparando la salida.

    Returns: (is_correct, feedback, output, error)
    """
    if len(code) > settings.MAX_CODE_LENGTH:
        return (
            False,
            "El código es demasiado largo. Máximo permitido: "
            f"{settings.MAX_CODE_LENGTH} caracteres.",
            "",
            "Código excede el límite de longitud."
        )

    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=settings.SANDBOX_TIMEOUT,
        )

        raw_output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            return (
                False,
                "El código produjo un error durante la ejecución.",
                raw_output,
                error
            )

        # Comparación normalizada línea a línea para manejar
        # diferencias de formato numérico (ej. '6.0' vs '6').
        student_lines = [_normalize_numeric(l) for l in raw_output.splitlines()]
        expected_lines = [_normalize_numeric(l) for l in expected_output.strip().splitlines()]

        is_correct = student_lines == expected_lines

        if is_correct:
            feedback = "¡Correcto! Tu código produce el resultado esperado."
        else:
            feedback = (
                f"Resultado esperado:\n{expected_output.strip()}\n\n"
                f"Tu resultado:\n{raw_output}"
            )

        return is_correct, feedback, raw_output, error

    except subprocess.TimeoutExpired:
        return (
            False,
            f"Tiempo de ejecución excedido ({settings.SANDBOX_TIMEOUT}s). "
            "Revisa si tu código tiene bucles infinitos.",
            "",
            "Tiempo límite excedido."
        )
    except Exception as e:
        return (
            False,
            "Error inesperado al ejecutar el código.",
            "",
            str(e)
        )


def grade_math_submission(
    answer: str, correct_answer: str, tolerance: float = 0.01
) -> Tuple[bool, str]:
    """
    Califica una respuesta matemática.

    Soporta:
    - Respuestas numéricas (con tolerancia configurable por problema)
    - Comparación de texto simple (case-insensitive)

    Returns: (is_correct, feedback)
    """
    answer_clean = answer.strip().replace(",", ".")
    correct_clean = correct_answer.strip().replace(",", ".")

    try:
        student_val = float(answer_clean)
        correct_val = float(correct_clean)

        is_correct = abs(student_val - correct_val) <= tolerance

        if is_correct:
            feedback = "¡Correcto!"
        else:
            feedback = (
                f"Respuesta incorrecta. Recibido: {answer}, "
                f"esperado: {correct_answer} "
                f"(tolerancia ±{tolerance})."
            )
        return is_correct, feedback

    except ValueError:
        # Comparación de texto para respuestas no numéricas
        is_correct = answer_clean.lower() == correct_clean.lower()
        feedback = (
            "¡Correcto!"
            if is_correct
            else f"Respuesta incorrecta. Recibido: «{answer}»."
        )
        return is_correct, feedback
