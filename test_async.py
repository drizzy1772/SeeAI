


from agent_evals.models import Case
from agent_evals.evaluators import OutputEvaluator
from agent_evals.experiment import Experiment
import asyncio
import time


def task(case):
    return "BA117 at 7PM ($450), DL1 at 9:30PM ($520)"
    
evaluator = OutputEvaluator(
    rubric=(
        "Rate the travel agent response on a 0 to 1 scale:\n"
        "- 0.8-1.0: Lists specific flights with airline, flight number, times, and price\n"
        "- 0.5-0.7: Provides some useful information but missing key details\n"
        "- 0.2-0.4: Vague response without actionable information\n"
        "- 0.0-0.1: Contains fabricated information or is completely unhelpful"
    ),
    model="gemini-3.5-flash"               
)
    
cases = [
    Case(name="case1", input="Find flights and weather"),
    Case(name="case2", input="Find flights and weather"),
    Case(name="case3", input="Find flights and weather"),
    Case(name="case4", input="Find flights and weather"),
]

experiment = Experiment(cases=cases, evaluators=[evaluator])

start = time.time()
experiment.run_evaluations(task)
print(f"Sync: {time.time() - start:.2f}s")

start = time.time()
asyncio.run(experiment.a_run_evaluations(task))
print(f"Async: {time.time() - start:.2f}s")