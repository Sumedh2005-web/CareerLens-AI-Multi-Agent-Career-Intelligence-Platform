import streamlit as st
from graph.workflow import run_pipeline

st.set_page_config(
    page_title="InternIQ",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 InternIQ — Multi-Agent Internship Market Analyst")
st.caption("Powered by LangGraph · Groq LLaMA 3.3 · PostgreSQL · 757 real Internshala listings")

st.markdown("---")

# Suggested questions
st.subheader("💡 Try asking:")
examples = [
    "What are the top 10 most in-demand skills?",
    "Average stipend by job category",
    "Which cities have the most internship opportunities?",
    "Remote vs on-site internship distribution",
    "Top companies hiring for data science internships",
    "Stipend range for internships requiring machine learning skills"
]

cols = st.columns(3)
for i, q in enumerate(examples):
    if cols[i % 3].button(q, use_container_width=True):
        st.session_state["question"] = q

st.markdown("---")

question = st.text_input(
    "Ask anything about the internship market:",
    value=st.session_state.get("question", ""),
    placeholder="e.g. Which skills have the highest stipend?"
)

if st.button("🔍 Analyse", type="primary") and question.strip():
    with st.spinner("Agents working..."):

        col_status = st.empty()

        col_status.info("🗂️ Planner → breaking down your question...")
        result = run_pipeline(question)

    if result.get("error"):
        st.error(f"SQL Error: {result['error']}")
        st.code(result["sql"], language="sql")
    else:
        # Layout
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📊 Visualisation")
            if result["figure"]:
                st.plotly_chart(result["figure"], use_container_width=True)
            else:
                st.warning("No chart generated for this query.")

        with col2:
            st.subheader("🔍 Generated SQL")
            st.code(result["sql"], language="sql")

            st.subheader("📋 Raw Results")
            import pandas as pd
            if result["results"]:
                st.dataframe(
                    pd.DataFrame(result["results"]),
                    use_container_width=True,
                    height=200
                )

        st.markdown("---")
        st.subheader("💼 Business Insight")
        st.success(result["insight"])
