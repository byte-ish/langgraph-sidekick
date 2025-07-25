from .state import State

def worker_router(state: State) -> str:
    """Decide next node after worker."""
    last_message = state["messages"][-1]
    return "tools" if hasattr(last_message, "tool_calls") and last_message.tool_calls else "evaluator"

def route_based_on_evaluation(state: State) -> str:
    if state["success_criteria_met"] or state["user_input_needed"]:
        return "END"
    else:
        return "worker"