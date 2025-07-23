
## ✅ Step 2 — Use This Full Working Code  

import google.generativeai as genai
import sqlite3

genai.configure(api_key="TYPE YOUR API KEY")
model = genai.GenerativeModel('gemini-2.5-pro')

def get_sql_from_question(question):
    prompt = (
        f"Write a valid SQLite SQL query to answer this question: '{question}'. "
        "Assume the table name is 'product_sales'. Return only the SQL query."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

def clean_sql_query(sql_query):
    return sql_query.replace("```sql", "").replace("```", "").strip()

def execute_sql(sql_query):
    try:
        conn = sqlite3.connect('ecommerce.db')
        result = conn.execute(sql_query).fetchall()
        conn.close()
        return result
    except Exception as e:
        return f"Error executing SQL: {e}"

# Main Program
question = (
    "The table 'product_sales' has columns: date (TEXT), item_id (INTEGER), "
    "total_sales (REAL), total_units_ordered (INTEGER). "
    "Write an SQLite query to calculate the total sales from this table."
)
raw_sql = get_sql_from_question(question)
print("\n✅ Generated SQL Query:\n", raw_sql)

cleaned_sql = clean_sql_query(raw_sql)
print("\n✅ Cleaned SQL Query:\n", cleaned_sql)

result = execute_sql(cleaned_sql)
print("\n✅ Query Result:", result)
import sqlite3

conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(product_sales);")
columns = cursor.fetchall()

conn.close()

print("\n✅ Columns in 'product_sales' table:")
for column in columns:
    print(f"- {column[1]} ({column[2]})")

import matplotlib.pyplot as plt

def plot_total_sales(total_sales):
    plt.bar(['Total Sales'], [total_sales])
    plt.ylabel('Sales Amount')
    plt.title('Total Sales Report')
    plt.show()

plot_total_sales(1004904.56)

