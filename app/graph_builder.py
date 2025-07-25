from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from .state import State
from .worker import worker
from .evaluator import evaluator
from .tools import tools
from .router import worker_router, route_based_on_evaluation

def build_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("worker", worker)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    graph_builder.add_node("evaluator", evaluator)

    graph_builder.add_conditional_edges("worker", worker_router, {"tools": "tools", "evaluator": "evaluator"})
    graph_builder.add_edge("tools", "worker")
    graph_builder.add_conditional_edges("evaluator", route_based_on_evaluation, {"worker": "worker", "END": END})
    graph_builder.add_edge(START, "worker")

    memory = MemorySaver()
    return graph_builder.compile(checkpointer=memory)