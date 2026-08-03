






from agent_evals.models import Case
from agent_evals.evaluators import TrajectoryEvaluator
import pytest

@pytest.fixture
def trajectory_evaluator():
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
    return evaluator

def test_efficient_trajectory_scores_high(trajectory_evaluator):
    case = Case(name="efficient", input="Find flights and weather")
    report = trajectory_evaluator.evaluate(case, "some output", trajectory=[{"name": "search_flights", "args": {}}, {"name": "get_weather", "args": {}}])
    assert report.success

def test_wasteful_trajectory_scores_low(trajectory_evaluator):
    case = Case(name="wasteful", input="Find flights and weather")
    wasteful_trajectory = [
        {"name": "search_flights", "args": {}},
        {"name": "get_currency_exchange", "args": {}},
        {"name": "search_flights", "args": {}},
        {"name": "get_weather", "args": {}},
    ]
    report = trajectory_evaluator.evaluate(case, "some output", trajectory=wasteful_trajectory)
    assert report.success == False