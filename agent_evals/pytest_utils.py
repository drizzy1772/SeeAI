

from agent_evals.models import Report
import warnings



def assert_test(report: Report, threshold: float = 0.8) -> None:
    if report.overall_score >= threshold:
        return

    message = (
        f"Case failed: {report.case_name}\n"
        f"Judge: {report.evaluator_name}\n"
        f"Score: {report.overall_score}\n"
        f"Reasoning: {report.reasoning}\n"
    )
    
    if report.is_flaky:
        return warnings.warn(f"{message}", UserWarning)
    else:
        raise AssertionError(message)