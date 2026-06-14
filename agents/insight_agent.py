import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from db.connection import get_config
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_config("GROQ_API_KEY"),
    temperature=0.3
)

def run_insight_agent(question: str, sql: str, results: list[dict]) -> str:
    if not results:
        return "No data returned. Try rephrasing your question."

    df = pd.DataFrame(results)
    summary = df.head(10).to_string(index=False)

    prompt = f"""You are a business analyst for an internship market platform.

User asked: {question}

SQL used: {sql}

Top results:
{summary}

Write 2-3 sentences of sharp business insight from this data.
Focus on what's actionable for a job seeker or recruiter.
No filler. No restating the question. Just insight."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
