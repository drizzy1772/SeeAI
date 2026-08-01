



from typing import Optional, List, Dict, Any
from .models import Case, Report
from google import genai
from google.genai import types
import json

class BaseEvaluator:
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, case: Case, actual_output: str, trajectory: Optional[List[Dict[str, Any]]] = None) -> Report:
        raise NotImplementedError("Subclasses must implement evaluate()")
    
class OutputEvaluator(BaseEvaluator):
    def __init__(self, rubric: str, model: str = "gemini-3.5-flash"):
        super().__init__(name="OutputEvaluator")
        self.rubric = rubric
        self.model = model
        self.client = genai.Client()
    
    def evaluate(self, case: Case, actual_output: str, trajectory: Optional[List[Dict[str, Any]]] = None) -> Report:
        promt = (
            "You are an AI judge. Evaluate the agent's response based strictly on the provided rubric. \n"
            f"Rubric:\n{self.rubric}\n\n"
            "Return a JSON object with exactly two keys:\n"
            "- 'score': a float between 0.0 and 1.0\n"
            "- 'reasoning': a brief string explaining why you gave this score." 
        )
        
        user_promt = f"Task: {case.input}\nAgent response: {actual_output}"
        
        try:
            response = self.client.models.generate_content( 
                model = self.model,
                contents=user_promt,
                config=types.GenerateContentConfig(
                    system_instruction=promt,
                    response_mime_type="application/json",
                )
            )
        
            result = json.loads(response.text)
            score = float(result.get("score", 0.0))
            reasoning = result.get("reasoning", "No reasoning Provided")
        except Exception as e:
            score = 0.0
            reasoning = f"Judge failed: {str(e)}"
        
        return Report(
            case_name=case.name,
            overall_score=score,
            reasoning=reasoning,
            evaluator_name=self.name
        )
        
        
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











            