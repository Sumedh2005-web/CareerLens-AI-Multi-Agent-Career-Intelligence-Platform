from graph.workflow import run_pipeline

result = run_pipeline("What are the top 10 most in-demand skills?")

print("Status:", result["status"])
print("SQL:", result["sql"])
print("Rows:", len(result["results"]))
print("Fig:", type(result["figure"]))
print("Insight:", result["insight"])
