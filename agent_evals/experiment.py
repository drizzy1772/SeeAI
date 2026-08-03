

from typing import List, Callable, Any
from .models import Case, Report
from .evaluators import BaseEvaluator
import asyncio

class Experiment:
    def __init__(self, cases: List[Case], evaluators: List[BaseEvaluator]):
        self.cases = cases
        self.evaluators = evaluators

    def run_evaluations(self, task_func: Callable):
        twin = []
        
        for case in self.cases:
            result = task_func(case)
            if isinstance(result, dict):
                actual_output = result["output"]
                trajectory = result["trajectory"]
            else:
                actual_output = result
                trajectory = None
        
            for evaluator in self.evaluators:
                report = evaluator.evaluate(case, actual_output, trajectory)
                twin.append(report)
        return twin
    
    async def a_run_evaluations(self, task_func):
        twin = []
        
        for case in self.cases:
            result = task_func(case)
            if isinstance(result, dict):
                actual_output = result["output"]
                trajectory = result["trajectory"]
            else:
                actual_output = result
                trajectory = None
    

            for evaluator in self.evaluators:
                coroutine = evaluator.a_evaluate(case, actual_output, trajectory)
                twin.append(coroutine)
        
        results = await asyncio.gather(*twin)
        return results