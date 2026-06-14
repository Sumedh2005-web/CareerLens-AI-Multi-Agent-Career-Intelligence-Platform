SCHEMA_CONTEXT = """
You are an expert SQL analyst for an internship market database.

Tables:
1. jobs (id, internship_id, title, company, location, stipend_min, stipend_max,
         duration, posted, job_type, description, is_remote, category, scraped_at)
2. job_skills (id, internship_id, skill)

Rules:
- Join tables on internship_id
- stipend_min and stipend_max are numeric (monthly INR)
- is_remote is boolean
- Always use LIMIT 100 max
- Return only the SQL query, no explanation
- Use lowercase column names exactly as shown
"""

FEW_SHOT_EXAMPLES = [
    {
        "question": "What are the top 10 most in-demand skills?",
        "sql": """
SELECT skill, COUNT(*) as demand_count
FROM job_skills
GROUP BY skill
ORDER BY demand_count DESC
LIMIT 10;
"""
    },
    {
        "question": "Average stipend by job category",
        "sql": """
SELECT category,
       ROUND(AVG(stipend_min)::numeric, 0) as avg_min_stipend,
       ROUND(AVG(stipend_max)::numeric, 0) as avg_max_stipend,
       COUNT(*) as total_jobs
FROM jobs
WHERE stipend_min IS NOT NULL
GROUP BY category
ORDER BY avg_min_stipend DESC;
"""
    },
    {
        "question": "Which cities have the most internship opportunities?",
        "sql": """
SELECT location, COUNT(*) as opportunity_count
FROM jobs
GROUP BY location
ORDER BY opportunity_count DESC
LIMIT 10;
"""
    },
    {
        "question": "Top companies hiring for data science internships",
        "sql": """
SELECT j.company, COUNT(*) as openings,
       ROUND(AVG(j.stipend_min)::numeric, 0) as avg_stipend
FROM jobs j
JOIN job_skills js ON j.internship_id = js.internship_id
WHERE LOWER(js.skill) LIKE '%python%'
   OR LOWER(j.category) LIKE '%data%'
GROUP BY j.company
ORDER BY openings DESC
LIMIT 10;
"""
    },
    {
        "question": "Remote vs on-site internship distribution",
        "sql": """
SELECT
    CASE WHEN is_remote THEN 'Remote' ELSE 'On-site' END as work_type,
    COUNT(*) as count,
    ROUND(AVG(stipend_min)::numeric, 0) as avg_stipend
FROM jobs
GROUP BY is_remote;
"""
    },
    {
        "question": "Stipend range for internships requiring machine learning skills",
        "sql": """
SELECT j.title, j.company, j.location,
       j.stipend_min, j.stipend_max, j.duration
FROM jobs j
JOIN job_skills js ON j.internship_id = js.internship_id
WHERE LOWER(js.skill) LIKE '%machine learning%'
  AND j.stipend_min IS NOT NULL
ORDER BY j.stipend_min DESC
LIMIT 20;
"""
    }
]

def build_prompt(user_question: str) -> str:
    examples_text = ""
    for ex in FEW_SHOT_EXAMPLES:
        examples_text += f"\nQuestion: {ex['question']}\nSQL: {ex['sql']}\n"

    return f"""{SCHEMA_CONTEXT}

Examples:
{examples_text}

Now generate SQL for this question:
Question: {user_question}
SQL:"""
