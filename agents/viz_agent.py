import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def run_viz_agent(results: list[dict], question: str) -> go.Figure:
    if not results:
        return None

    df = pd.DataFrame(results)
    cols = df.columns.tolist()
    q = question.lower()

    # Detect numeric and categorical columns
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    if not num_cols:
        return None

    x_col = cat_cols[0] if cat_cols else cols[0]
    y_col = num_cols[0]

    # Chart type selection logic
    if any(w in q for w in ["trend", "over time", "monthly", "weekly", "posted"]):
        fig = px.line(df, x=x_col, y=y_col, title=question)

    elif any(w in q for w in ["distribution", "remote", "vs", "ratio", "type"]):
        fig = px.pie(df, names=x_col, values=y_col, title=question)

    elif any(w in q for w in ["compare", "range", "min", "max", "stipend"]) and len(num_cols) >= 2:
        fig = px.bar(
            df, x=x_col, y=num_cols,
            barmode="group", title=question
        )

    else:
        # Default: horizontal bar (best for ranked lists)
        df_sorted = df.sort_values(y_col, ascending=True).tail(15)
        fig = px.bar(
            df_sorted, x=y_col, y=x_col,
            orientation="h", title=question
        )

    fig.update_layout(
        plot_bgcolor="#0f1117",
        paper_bgcolor="#0f1117",
        font_color="#ffffff",
        title_font_size=14,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig
