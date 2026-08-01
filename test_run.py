




from agent_evals.models import Case
from agent_evals.evaluators import OutputEvaluator
from agent_evals.experiment import Experiment

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
    Case(name="good", input="Find flights NYC to London",
        expected_output="Specific flights with details"),
    Case(name="vague", input="Find flights NYC to London",
         expected_output="Specific flights with details"),
]

def task(case: Case):
    if case.name == "good":
        return "BA117 at 7PM ($450), DL1 at 9:30PM ($520)"
    return "There are several flights available. Prices vary."

experiment = Experiment(cases=cases, evaluators=[evaluator])
reports = experiment.run_evaluations(task)

for report in reports:
    report.display()

