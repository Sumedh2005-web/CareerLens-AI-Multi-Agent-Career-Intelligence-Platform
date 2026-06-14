from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.sql_agent import run_sql_agent
from agents.viz_agent import run_viz_agent
from agents.insight_agent import run_insight_agent
import plotly.graph_objects as go

class AgentState(TypedDict):
    question: str
    sql: str
    results: list
    error: Optional[str]
    figure: Optional[go.Figure]
    insight: str
    status: str

def planner_node(state: AgentState) -> AgentState:
    state["status"] = "planning"
    return state

def sql_node(state: AgentState) -> AgentState:
    state["status"] = "querying"
    out = run_sql_agent(state["question"])
    state["sql"] = out["sql"]
    state["results"] = out["results"]
    state["error"] = out["error"]
    return state

def viz_node(state: AgentState) -> AgentState:
    state["status"] = "visualizing"
    state["figure"] = run_viz_agent(state["results"], state["question"])
    return state

def insight_node(state: AgentState) -> AgentState:
    state["status"] = "analyzing"
    state["insight"] = run_insight_agent(
        state["question"], state["sql"], state["results"]
    )
    return state

def should_continue(state: AgentState) -> str:
    if state.get("error") or not state.get("results"):
        return "end"
    return "viz"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("sql", sql_node)
    graph.add_node("viz", viz_node)
    graph.add_node("insight", insight_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "sql")
    graph.add_conditional_edges("sql", should_continue, {
        "viz": "viz",
        "end": END
    })
    graph.add_edge("viz", "insight")
    graph.add_edge("insight", END)

    return graph.compile()

pipeline = build_graph()

def run_pipeline(question: str) -> AgentState:
    return pipeline.invoke({
        "question": question,
        "sql": "",
        "results": [],
        "error": None,
        "figure": None,
        "insight": "",
        "status": "idle"
    })
