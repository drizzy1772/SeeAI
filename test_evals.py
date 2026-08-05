

import pytest
from agent_evals.models import Case
from agent_evals.pytest_utils import assert_test 
from agent_evals.evaluators import OutputEvaluator


TEST_CASES = [
    Case(name="Success case", input="Return the word 'good'", expected_output="good", flaky=False),
    Case(name="Middle case", input="Not on the way", expected_output="50/50", flaky=True)
    ]

def my_agent(input_text: str) -> str:
    if "Not" in input_text:
        return "bad"
    return "good"

@pytest.mark.asyncio
@pytest.mark.parametrize("case", TEST_CASES)
async def test_agent_evals(case: Case):
    evaluator = OutputEvaluator(
        rubric=
        "You are an AI judge. Compare the agent's actual output with the expected_output. "
        "Return ONLY a valid JSON object without any markdown formatting or backticks. "
        "Do not use nested double quotes inside the strings. "
        "Exactly two keys required:\n"
        "- 'score': 1.0 if the output matches the expected_output, else 0.0\n"
        "- 'reasoning': a brief explanation without double quotes."
    )
    
    result = my_agent(case.input)
    
    report = await evaluator.a_evaluate(case, result)
    
    report.is_flaky = case.flaky
    
    assert_test(report)