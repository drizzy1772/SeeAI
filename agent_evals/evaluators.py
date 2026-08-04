



from typing import Optional, List, Dict, Any
from .models import Case, Report
from google import genai
from google.genai import types
import json
import asyncio

class BaseEvaluator:
    def __init__(self, name: str):
        self.name = name
        self.cache = {}
        
    def evaluate(self, case: Case, actual_output: str, trajectory: Optional[List[Dict[str, Any]]] = None) -> Report:
        raise NotImplementedError("Subclasses must implement evaluate()")
    
class OutputEvaluator(BaseEvaluator):
    def __init__(self, rubric: str, model: str = "gemini-3.5-flash"):
        super().__init__(name="OutputEvaluator")
        self.rubric = rubric
        self.model = model
        self.client = genai.Client()
    
    def evaluate(self, case: Case, actual_output: str, trajectory: Optional[List[Dict[str, Any]]] = None) -> Report:
        cache_key = f"{case.name}:{actual_output}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]

        
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
        
        report = Report(
            case_name=case.name,
            overall_score=score,
            reasoning=reasoning,
            evaluator_name=self.name,
            model=self.model,
            hyperparameters={"rubric": self.rubric}  
        )
        self.cache[cache_key] = report
        return report
    
    async def a_evaluate(self, case: Case, actual_output: str, trajectory: Optional[List[Dict[str, Any]]] = None) -> Report:
            promt = (
                "You are an AI judge. Evaluate the agent's response based strictly on the provided rubric. \n"
                f"Rubric:\n{self.rubric}\n\n"
                "Return a JSON object with exactly two keys:\n"
                "- 'score': a float between 0.0 and 1.0\n"
                "- 'reasoning': a brief string explaining why you gave this score." 
            )
            
            user_promt = f"Task: {case.input}\nAgent response: {actual_output}"
            
            try:
                response = await self.client.aio.models.generate_content( 
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
                evaluator_name=self.name,
                model=self.model,
                hyperparameters={"rubric": self.rubric}
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
    
    async def a_evaluate(self, case, actual_output, trajectory=None):
        return self.evaluate(case, actual_output, trajectory)
    
class ToolCalled(BaseEvaluator):
    def __init__(self, tool_name: str):
        super().__init__(name="ToolCalled")
        self.tool_name = tool_name
        
    def evaluate(self, case: Case, actual_output: str, trajectory = None):
        if trajectory is None:
            result = Report(
            case_name=case.name,
            overall_score=0.0,
            reasoning="No trajectory provided",
            evaluator_name=self.name,
            )
            return result
        
        else:
            found = False
            for tool_call in trajectory:
                if tool_call["name"] == self.tool_name:
                    found = True
                    break
            if found:
                score=1.0
                reasoning="Tool found"
            else:
                score=0.0
                reasoning="Tool was not found"
                
            return Report(
                case_name=case.name,
                overall_score=score,
                reasoning=reasoning,
                evaluator_name=self.name
            )
    async def a_evaluate(self, case, actual_output, trajectory=None):
        return self.evaluate(case, actual_output, trajectory)
    
class TrajectoryEvaluator(BaseEvaluator):
    def __init__(self, rubric: str, model: str = "gemini-3.5-flash"):
        super().__init__(name="TrajectoryEvaluator")
        self.rubric = rubric
        self.model = model
        self.client = genai.Client()
    
    def evaluate(self, case: Case, actual_output: str, trajectory = None):
        cache_key = f"{case.name}:{json.dumps(trajectory)}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
                    
        
        
        if trajectory is None:
            result = Report(
                case_name=case.name,
                overall_score=0.0,
                reasoning="No trajectory provided",
                evaluator_name=self.name
            )
            return result

        promt = (
            "You are an AI judge. Evaluate the agent's tool-call trajectory \n"
            f"Rubric:\n{self.rubric}\n\n"
            "Return a JSON object with exactly two keys:\n"
            "- 'score': a float between 0.0 and 1.0\n"
            "- 'reasoning': a brief string explaining why you gave this score."
        )
        user_promt = f"Task: {case.input}\nAgent response: {json.dumps(trajectory)}"
        
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
            reasoning = result.get('reasoning', "No reasoning provided")
        except Exception as e:
            score = 0.0
            reasoning = f"Judge failed: {str(e)}"
            
        report = Report(
            case_name=case.name,
            overall_score=score,
            reasoning=reasoning,
            evaluator_name=self.name,
            model=self.model,
            hyperparameters={"rubric": self.rubric}
        )
        self.cache[cache_key] = report
        return report
    
    async def a_evaluate(self, case: Case, actual_output: str, trajectory=None):
        if trajectory is None:
                    result = Report(
                        case_name=case.name,
                        overall_score=0.0,
                        reasoning="No trajectory provided",
                        evaluator_name=self.name
                    )
                    return result
        
        promt = (
            "You are an AI judge. Evaluate the agent's tool-call trajectory \n"
            f"Rubric:\n{self.rubric}\n\n"
            "Return a JSON object with exactly two keys:\n"
            "- 'score': a float between 0.0 and 1.0\n"
            "- 'reasoning': a brief string explaining why you gave this score."
        )
        user_promt = f"Task: {case.input}\nAgent response: {json.dumps(trajectory)}"
                
        try:
            response = await self.client.aio.models.generate_content(
                model = self.model,
                contents=user_promt,
                config=types.GenerateContentConfig(
                    system_instruction=promt,
                    response_mime_type="application/json",
                )
            )
            result = json.loads(response.text)
            score = float(result.get("score", 0.0))
            reasoning = result.get('reasoning', "No reasoning provided")
        except Exception as e:
            score = 0.0
            reasoning = f"Judge failed: {str(e)}"
            
        return Report(
            case_name=case.name,
            overall_score=score,
            reasoning=reasoning,
            evaluator_name=self.name,
            model=self.model,
            hyperparameters={"rubric": self.rubric}
        )