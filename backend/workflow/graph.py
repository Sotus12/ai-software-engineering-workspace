from typing import Dict, Any, Literal
try:
    from langgraph.graph import StateGraph, START, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

from backend.workflow.state import ProjectState
from backend.agents import (
    run_requirement_agent,
    run_architecture_agent,
    run_developer_agent,
    run_testing_agent,
    run_review_agent
)

def route_after_testing(state: ProjectState) -> str:
    """
    Conditional Router defined by Person 1:
    Routes flow back to Developer Agent if tests fail and retry limit is not exceeded.
    Otherwise forwards to Code Review Agent.
    """
    test_results = state.get("test_results", {})
    passed = test_results.get("passed", True)
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)

    if passed or retry_count >= max_retries:
        return "review"
    else:
        # Increment retry counter before looping back to developer
        state["retry_count"] = retry_count + 1
        return "developer"

def build_orchestrator():
    """
    Builds and compiles the multi-agent LangGraph workflow.
    """
    if not LANGGRAPH_AVAILABLE:
        return None

    builder = StateGraph(ProjectState)

    # Add agent nodes
    builder.add_node("requirement", run_requirement_agent)
    builder.add_node("architecture", run_architecture_agent)
    builder.add_node("developer", run_developer_agent)
    builder.add_node("testing", run_testing_agent)
    builder.add_node("review", run_review_agent)

    # Define linear edge sequence
    builder.add_edge(START, "requirement")
    builder.add_edge("requirement", "architecture")
    builder.add_edge("architecture", "developer")
    builder.add_edge("developer", "testing")

    # Define conditional feedback loop
    builder.add_conditional_edges(
        "testing",
        route_after_testing,
        {
            "review": "review",
            "developer": "developer"
        }
    )
    builder.add_edge("review", END)

    return builder.compile()

def run_orchestrator(initial_state: ProjectState) -> ProjectState:
    """
    Executes the multi-agent workflow for a given project state.
    """
    state = dict(initial_state)
    
    if LANGGRAPH_AVAILABLE:
        app = build_orchestrator()
        if app is not None:
            return app.invoke(state)
            
    # Sequential fallback execution loop when LangGraph module is loading
    state = run_requirement_agent(state)
    state = run_architecture_agent(state)
    
    while True:
        state = run_developer_agent(state)
        state = run_testing_agent(state)
        
        next_node = route_after_testing(state)
        if next_node == "review":
            break
            
    state = run_review_agent(state)
    state["status"] = "COMPLETED"
    return state
