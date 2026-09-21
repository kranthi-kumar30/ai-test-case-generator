import streamlit as st
from src.generator import DEFAULT_COVERAGE, TestCaseGenerator

st.set_page_config(page_title="AI Test Case Generator", page_icon="🧪", layout="wide")
st.title("🧪 AI Test Case Generator")
st.caption("Generate structured QA test cases from requirements, user stories, and acceptance criteria.")

with st.sidebar:
    st.header("Generation settings")
    coverage = st.multiselect(
        "Coverage types",
        ["Positive", "Negative", "Boundary", "Validation", "Security", "Usability", "Regression"],
        default=DEFAULT_COVERAGE,
    )
    max_cases = st.slider("Maximum test cases", 2, 12, 6)

default_requirement = """As a customer, I want to log in using email and password so that I can access my account.

Acceptance criteria:
- Email is required and must be valid.
- Password is required.
- Successful login redirects to the dashboard.
- Invalid credentials show an error.
- Account locks after five consecutive failed attempts.
"""

requirement = st.text_area(
    "Requirement / User Story / Acceptance Criteria",
    value=default_requirement,
    height=220,
)

if st.button("Generate Test Cases", type="primary"):
    try:
        generator = TestCaseGenerator()
        cases = generator.generate(requirement, coverage, max_cases)
        st.success(f"Generated {len(cases)} test cases.")

        for case in cases:
            with st.expander(f"{case.test_case_id} — {case.title}"):
                c1, c2 = st.columns(2)
                c1.write(f"**Priority:** {case.priority}")
                c2.write(f"**Type:** {case.test_type}")

                st.write("**Preconditions**")
                for item in case.preconditions:
                    st.write(f"- {item}")

                st.write("**Steps**")
                for i, step in enumerate(case.steps, 1):
                    st.write(f"{i}. {step}")

                st.write(f"**Expected Result:** {case.expected_result}")
                st.write(f"**Test Data:** {case.test_data}")

        output = generator.to_json(cases)
        st.download_button(
            "Download JSON",
            data=output,
            file_name="generated_test_cases.json",
            mime="application/json",
        )
        st.subheader("JSON Preview")
        st.code(output, language="json")
    except Exception as exc:
        st.error(str(exc))
