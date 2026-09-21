from .models import TestCase

def validate_requirement(requirement: str) -> None:
    if not requirement or not requirement.strip():
        raise ValueError("Requirement cannot be empty.")
    if len(requirement.strip()) < 15:
        raise ValueError("Requirement is too short. Add more context.")

def validate_test_cases(test_cases) -> None:
    cases = list(test_cases)
    if not cases:
        raise ValueError("No test cases were generated.")
    for case in cases:
        if not case.test_case_id.strip():
            raise ValueError("Each test case must have an ID.")
        if not case.title.strip():
            raise ValueError(f"{case.test_case_id}: title is missing.")
        if not case.steps:
            raise ValueError(f"{case.test_case_id}: steps are missing.")
        if not case.expected_result.strip():
            raise ValueError(f"{case.test_case_id}: expected result is missing.")
