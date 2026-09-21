from dataclasses import dataclass, asdict
from typing import List

@dataclass
class TestCase:
    test_case_id: str
    title: str
    priority: str
    test_type: str
    preconditions: List[str]
    steps: List[str]
    expected_result: str
    test_data: str

    def to_dict(self):
        return asdict(self)
