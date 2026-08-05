


from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class Case:
    name: str
    input: str
    expected_output: Optional[str] = None
    expected_trajectory: Optional[List[str]] = None
    flaky: bool = False
    
    
@dataclass
class Report:
    case_name: str
    overall_score: float 
    reasoning: str
    evaluator_name: str
    threshold: float = 0.5
    model: Optional[str] = None
    hyperparameters: Optional[dict] = None
    is_flaky: bool = False
    
    @property
    def success(self) -> bool:
        return self.overall_score >= self.threshold
    
    def display(self):
        status = "good" if self.success else "bad"
        print(f"[{self.evaluator_name}] {status} {self.case_name}: Score {self.overall_score:.2f} - {self.reasoning}")