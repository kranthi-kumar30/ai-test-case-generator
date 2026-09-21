import pytest
from src.generator import TestCaseGenerator
from src.validators import validate_requirement

def test_local_generator_returns_test_cases():
    generator = TestCaseGenerator()
    requirement = (
        "As a customer, I want to login using email and password. "
        "Valid credentials should redirect me to the dashboard."
    )
    cases = generator.generate(
        requirement=requirement,
        coverage_types=["Positive", "Negative", "Boundary"],
        max_cases=4,
    )
    assert len(cases) >= 3
    assert cases[0].test_case_id == "TC-001"
    assert all(case.title for case in cases)
    assert all(case.expected_result for case in cases)

def test_json_export():
    generator = TestCaseGenerator()
    cases = generator.generate(
        requirement="Users should be able to search products by keyword and see relevant results.",
        coverage_types=["Positive", "Negative"],
        max_cases=3,
    )
    output = generator.to_json(cases)
    assert '"test_case_id"' in output
    assert '"expected_result"' in output

def test_empty_requirement_rejected():
    with pytest.raises(ValueError):
        validate_requirement("")
