



from agent_evals.models import Case
from agent_evals.evaluators import Contains, ToolCalled
import pytest


def test_contains_find_string():
    evaluator = Contains(value="$")
    case = Case(name="good", input="Find flights NYC to London")
    report = evaluator.evaluate(case, "Price: $450")
    assert report.success == True

def test_contains_missing_string():
    evaluator = Contains(value="$")
    case = Case(name="okay", input="Find flights NYC to London")
    report = evaluator.evaluate(case, "no price here")
    assert report.success == False
    
def test_call_called_found():
    evaluator = ToolCalled(tool_name="search_flights")
    case = Case(name="found", input="Find flights NYC to London")
    report = evaluator.evaluate(case, "Price is found",  trajectory=[{"name": "search_flights", "args": {}}])
    assert report.success == True

def test_tool_called_missing():
    evaluator = ToolCalled(tool_name="search_flights")
    case = Case(name="missing", input="Find flights NYC to London")
    report = evaluator.evaluate(case, "Price is missing", trajectory=[{"name": "get_weather", "args": {}}])
    assert report.success == False