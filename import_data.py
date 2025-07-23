import pandas as pd
import sqlite3

# Step 1 — Read your CSV file into a DataFrame
df = pd.read_csv('Product-Level Eligibility Table (mapped).csv')

# Step 2 — Connect to SQLite database (it creates file if not exists)
conn = sqlite3.connect('ecommerce.db')

# Step 3 — Import DataFrame into SQL Table (creates table automatically)
df.to_sql('Eligibilty', conn, if_exists='replace', index=False)

# Step 4 — Optional: Check if data is inserted
result = conn.execute('SELECT * FROM product_sales LIMIT 5').fetchall()
print(result)

# Step 5 — Close the connection
conn.close()
