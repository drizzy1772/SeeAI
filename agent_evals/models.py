


from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class Case:
    name: str
    input: str
    expected_output: Optional[str] = None
    expected_trajectory: Optional[List[str]] = None

@dataclass
class Report:
    case_name: str
    overall_score: float # 0.0 -> 1.0
    reasoning: str
    evaluator_name: str
    
    def display(self):
        print(f"[{self.evaluator_name}] {self.case_name}: Score {self.overall_score:.2f} - {self.reasoning}")