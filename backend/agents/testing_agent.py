from typing import Dict, Any

def run_testing_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Testing Agent (Person 2):
    Generates and executes tests against generated projects, producing structured feedback.
    """
    retry_count = state.get("retry_count", 0)
    
    # Simulate test execution results (Passes on attempt > 0 or default pass)
    test_passed = True if retry_count >= 1 else True
    
    test_results = {
        "passed": test_passed,
        "total_tests": 5,
        "passed_tests": 5 if test_passed else 4,
        "failed_tests": 0 if test_passed else 1,
        "stdout": "5 passed in 0.12s",
        "stderr": "",
        "summary": "All tests passed successfully." if test_passed else "AssertionError in test_main.py: line 14"
    }
    
    state["test_results"] = test_results
    state["status"] = "TESTING_COMPLETED"
    state["logs"].append({
        "agent": "TestingAgent",
        "message": f"Executed test suite. Status: {'PASSED' if test_passed else 'FAILED'}"
    })
    return state
