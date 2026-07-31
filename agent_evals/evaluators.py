



from typing import Optional, List, Dict, Any
from .models import Case, Report

class BaseEvaluator:
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, case: Case, actual_output: str, trajectory: Optional[List[Dict[str, Any]]] = None) -> Report:
        raise NotImplementedError("Subclasses must implement evaluate()")
    
class OutputEvaluator(BaseEvaluator):
    def __init__(self, rubric: str, model: str = "gpt-4o-mini"):
        super().__init__(name="OutputEvaluator")
        self.rubric = rubric
        self.model = model
    
    def evaluate(self, case: Case, actual_output: str, trajectory: Optional[List[Dict[str, Any]]] = None) -> Report:
        muting = 0.95
        muting_explain = "Test Reasoning"
        result = Report(case_name=case.name, overall_score=muting, reasoning=muting_explain, evaluator_name=self.name)
    
        return result

class Contains(BaseEvaluator):
    def __init__(self, value: str):
        super().__init__(name="Contains")
        self.value = value

    def evaluate(self, case, actual_output, trajectory = None):
        if self.value in actual_output:
            score = 1.0
            reasoning = "String found"
        else:
            score = 0.0
            reasoning = "String not found"
        
        result = Report(case_name=case.name, overall_score=score, reasoning=reasoning, evaluator_name="Contains")

        return result











            