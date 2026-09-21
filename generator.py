import json
from pathlib import Path

from .llm_client import LLMClient
from .models import TestCase
from .validators import validate_requirement, validate_test_cases

DEFAULT_COVERAGE = ["Positive", "Negative", "Boundary", "Validation", "Security"]

class TestCaseGenerator:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client or LLMClient()

    def generate(self, requirement, coverage_types=None, max_cases=8):
        validate_requirement(requirement)
        coverage = list(coverage_types or DEFAULT_COVERAGE)

        if self.llm_client.is_enabled():
            try:
                cases = self._generate_with_llm(requirement, coverage, max_cases)
                validate_test_cases(cases)
                return cases
            except Exception:
                pass

        cases = self._generate_locally(requirement, coverage, max_cases)
        validate_test_cases(cases)
        return cases

    def _generate_with_llm(self, requirement, coverage, max_cases):
        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "test_case_prompt.txt"
        template = prompt_path.read_text(encoding="utf-8")
        prompt = template.format(
            requirement=requirement,
            coverage=", ".join(coverage),
            max_cases=max_cases,
        )
        raw = self.llm_client.generate(prompt)
        return [self._from_dict(item, i + 1) for i, item in enumerate(raw[:max_cases])]

    def _generate_locally(self, requirement, coverage, max_cases):
        text = " ".join(requirement.split())
        feature = self._feature_name(text)

        patterns = {
            "Positive": (
                f"Verify successful {feature} with valid input",
                "High",
                ["User is on the relevant application screen."],
                ["Enter valid input.", "Submit the workflow.", "Observe the application response."],
                f"The {feature} workflow completes successfully.",
                "Valid values that satisfy the acceptance criteria.",
            ),
            "Negative": (
                f"Verify {feature} behavior with invalid input",
                "High",
                ["User is on the relevant application screen."],
                ["Enter invalid input.", "Submit the workflow.", "Observe error handling."],
                "Invalid action is blocked and a clear error is displayed.",
                "Invalid, unsupported, or malformed values.",
            ),
            "Boundary": (
                f"Verify boundary values for {feature}",
                "Medium",
                ["Boundary conditions can be entered or simulated."],
                ["Test Min-1.", "Test Min.", "Test Max.", "Test Max+1."],
                "Only values inside the allowed boundary are accepted.",
                "Min-1, Min, Max, Max+1.",
            ),
            "Validation": (
                f"Verify required-field and format validation for {feature}",
                "High",
                ["User can submit incomplete data."],
                ["Leave required fields blank.", "Enter malformed data.", "Submit each variation."],
                "Correct validation messages are displayed and invalid submission is prevented.",
                "Blank and malformed values.",
            ),
            "Security": (
                f"Verify basic security handling for {feature}",
                "High",
                ["User input is accepted by the feature."],
                ["Enter harmless script-like and injection-like strings.", "Submit.", "Observe behavior."],
                "Unsafe input is rejected or safely handled without execution or data exposure.",
                "<script>alert(1)</script> and similar harmless test strings.",
            ),
            "Usability": (
                f"Verify user feedback and clarity for {feature}",
                "Low",
                ["User can complete the workflow."],
                ["Complete the workflow.", "Review labels, messages, and navigation feedback."],
                "Feedback is clear and the next user action is understandable.",
                "Standard valid input.",
            ),
            "Regression": (
                f"Verify existing behavior remains stable for {feature}",
                "Medium",
                ["A stable baseline behavior is known."],
                ["Execute the main happy path.", "Execute a common failure path.", "Compare to baseline."],
                "Existing supported behavior remains stable.",
                "Representative valid and invalid data.",
            ),
        }

        cases = []
        index = 1
        for test_type in coverage:
            if test_type not in patterns:
                continue
            title, priority, preconditions, steps, expected, test_data = patterns[test_type]
            cases.append(TestCase(
                test_case_id=f"TC-{index:03d}",
                title=title,
                priority=priority,
                test_type=test_type,
                preconditions=preconditions,
                steps=steps,
                expected_result=expected,
                test_data=test_data,
            ))
            index += 1
            if len(cases) >= max_cases:
                break

        if len(cases) < max_cases:
            cases.append(TestCase(
                test_case_id=f"TC-{index:03d}",
                title=f"Verify stated acceptance criteria for {feature}",
                priority="High",
                test_type="Acceptance",
                preconditions=["Feature is available in a test environment."],
                steps=[
                    "Review each acceptance criterion.",
                    "Map each criterion to observable behavior.",
                    "Execute each condition.",
                    "Record pass/fail evidence.",
                ],
                expected_result="Every stated acceptance criterion is satisfied.",
                test_data=text[:300],
            ))

        return cases[:max_cases]

    @staticmethod
    def _feature_name(text):
        lowered = text.lower()
        for keyword in ["login", "sign in", "checkout", "payment", "search", "registration", "signup"]:
            if keyword in lowered:
                return keyword.replace("sign in", "login").replace("signup", "registration")
        return "feature"

    @staticmethod
    def _from_dict(item, index):
        return TestCase(
            test_case_id=str(item.get("test_case_id") or f"TC-{index:03d}"),
            title=str(item.get("title") or "Generated test case"),
            priority=str(item.get("priority") or "Medium"),
            test_type=str(item.get("test_type") or "Functional"),
            preconditions=list(item.get("preconditions") or []),
            steps=list(item.get("steps") or []),
            expected_result=str(item.get("expected_result") or ""),
            test_data=str(item.get("test_data") or ""),
        )

    @staticmethod
    def to_json(test_cases):
        return json.dumps([case.to_dict() for case in test_cases], indent=2)
