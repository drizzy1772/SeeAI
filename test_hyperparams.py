

from agent_evals.models import Case
from agent_evals.evaluators import OutputEvaluator


evaluator = OutputEvaluator(
    rubric=("test rubric, content does not matter here"
    ),
    model="fake-model-that-does-not-exist"
)

case = Case(name="test", input="test input")
report = evaluator.evaluate(case, "some output")
print(report.model)
print(report.hyperparameters)
print(report.reasoning)