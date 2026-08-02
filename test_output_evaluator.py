





from agent_evals.models import Case
from agent_evals.evaluators import OutputEvaluator


def test_good_response_scores_high():
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
    case = Case(name="good", input="Find flights NYC to London")
    report = evaluator.evaluate(case, "BA117 at 7PM ($450), DL1 at 9:30PM ($520)")
    assert report.success

def test_vague_response_scores_low():
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
    case = Case(name="vague", input="Find flights NYC to London")
    report = evaluator.evaluate(case, "There are several flights available. Prices vary.")
    assert report.success == False