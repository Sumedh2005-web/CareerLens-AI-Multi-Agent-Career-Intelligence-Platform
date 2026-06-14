import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from db.connection import run_query, get_config
from prompts.few_shot import build_prompt

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_config("GROQ_API_KEY"),
    temperature=0
)

def extract_sql(raw: str) -> str:
    raw = re.sub(r"```sql|```", "", raw).strip()
    if ";" in raw:
        raw = raw[:raw.index(";") + 1]
    return raw.strip()

def run_sql_agent(question: str) -> dict:
    prompt = build_prompt(question)
    response = llm.invoke([HumanMessage(content=prompt)])
    sql = extract_sql(response.content)
    try:
        results = run_query(sql)
        return {"question": question, "sql": sql, "results": results, "error": None}
    except Exception as e:
        return {"question": question, "sql": sql, "results": [], "error": str(e)}
