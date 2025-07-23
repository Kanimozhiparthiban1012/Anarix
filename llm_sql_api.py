from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import sqlite3
import os

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyB4wx30TgT6HeG8oJpuRDG5ZLdliBbnm3Q")
gemini_model = genai.GenerativeModel('gemini-2.5-pro')

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

# ✅ Clean Gemini SQL
def clean_sql_query(sql_query):
    return sql_query.replace("```sql", "").replace("```", "").strip()

# ✅ Gemini SQL Generator with All 3 Tables Mentioned
def get_sql_from_gemini(question):
    prompt = (
        "You are a SQL assistant for an e-commerce company. "
        "You can only write queries using these SQLite tables:\n"
        "- product_sales(date, item_id, total_sales, total_units_ordered)\n"
        "- ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold, cpc)\n"
        "- eligibility(item_id, eligible_status)\n\n"
        f"Convert this question into a valid SQLite query: '{question}'. "
        "Use 'item_id' instead of 'product_id' in all queries. "
        "Return only the SQL query without explanation."
    )
    response = gemini_model.generate_content(prompt)
    return clean_sql_query(response.text.strip())

# ✅ Execute SQL in SQLite
def execute_sql(sql_query):
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return f"SQL Error: {e}"

# ✅ Human Readable Answer Formatter
def format_answer(question, sql_query, sql_result):
    if isinstance(sql_result, str):
        return sql_result
    if not sql_result or not sql_result[0]:
        return "Sorry, no results found."
    answer = sql_result[0][0]
    return (
        f"✅ You asked: '{question}'\n"
        f"✅ SQL Used: {sql_query}\n"
        f"✅ Answer: {answer}"
    )

# ✅ FastAPI Endpoint
@app.post("/ask")
def ask_ai_agent(request: QuestionRequest):
    try:
        sql_query = get_sql_from_gemini(request.question)
        cleaned_sql = clean_sql_query(sql_query)
        result = execute_sql(cleaned_sql)
        human_readable = format_answer(request.question, cleaned_sql, result)
        return {
            "question": request.question,
            "generated_sql": cleaned_sql,
            "result": result,
            "human_readable_answer": human_readable
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Helper to Print DB Path and Columns
def print_db_info():
    db_path = os.path.abspath('ecommerce.db')
    print(f"✅ Your FastAPI is using this database: {db_path}")

    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(ad_sales);")
    columns = cursor.fetchall()
    print("\n✅ Columns in 'ad_sales' table:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")

    cursor.execute("SELECT item_id, cpc FROM ad_sales;")
    rows = cursor.fetchall()
    print("\n✅ Data in 'ad_sales' (item_id, cpc):")
    for row in rows:
        print(row)

    conn.close()

# ✅ Call this function manually when you want to debug the DB
#uvicorn llm_sql_api:app --reload
#print_db_info()
import sqlite3

conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Drop the existing ad_sales table if it exists
cursor.execute("DROP TABLE IF EXISTS ad_sales;")

# Recreate with correct columns including cpc
cursor.execute("""
CREATE TABLE ad_sales (
  date TEXT,
  item_id INTEGER,
  ad_sales REAL,
  impressions INTEGER,
  ad_spend REAL,
  clicks INTEGER,
  units_sold INTEGER,
  cpc REAL
);
""")

# Insert sample data with cpc values
sample_data = [
    ('2025-07-22', 101, 5000, 1000, 2000, 300, 50, 3.50),
    ('2025-07-22', 102, 7000, 2000, 2500, 400, 80, 4.20),
    ('2025-07-22', 103, 8000, 1500, 3000, 350, 70, 2.90)
]

cursor.executemany("""
INSERT INTO ad_sales (date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold, cpc)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", sample_data)

conn.commit()
conn.close()

print("✅ ad_sales table recreated with cpc column and sample data inserted.")
