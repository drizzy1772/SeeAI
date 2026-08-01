


from agent_evals.models import Case
from agent_evals.evaluators import TrajectoryEvaluator
from agent_evals.experiment import Experiment


evaluator = TrajectoryEvaluator(
    rubric=(
        "Rate the tool usage trajectory 0-1:\n"
        "- 0.8-1.0: Only relevant tools called, no duplicates, logical order\n"
        "- 0.5-0.7: Mostly correct but minor inefficiency\n"
        "- 0.2-0.4: Irrelevant tools called or excessive duplicates\n"
        "- 0.0-0.1: Completely wrong tool selection"
    ),
    model="gemini-3.5-flash"
)

efficient_trajectory = [
    {"name": "search_flights", "args": {"origin": "NYC", "dest": "London"}},
    {"name": "get_weather", "args": {"city": "London"}},
]

wasteful_trajectory = [
     {"name": "search_flights", "args": {"origin": "NYC", "dest": "London"}},
    {"name": "get_currency_exchange", "args": {}},
    {"name": "search_flights", "args": {"origin": "NYC", "dest": "London"}},
    {"name": "get_weather", "args": {"city": "London"}},
]

cases = [
    Case(name="efficient", input="Find flights and weather",
         expected_trajectory=["search_flights", "get_weather"]),
    Case(name="wasteful", input="Find flights and weather",
         expected_trajectory=["search_flights", "get_weather"])
]

def traj_task(case):
    trajectory = efficient_trajectory if case.name == "efficient" else wasteful_trajectory
    return {"output": "BA117 at 7PM, London is 18C", "trajectory": trajectory}

exp = Experiment(cases=cases, evaluators=[evaluator])
reports = exp.run_evaluations(traj_task)
for report in reports:
    report.display()