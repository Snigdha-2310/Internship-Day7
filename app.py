import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to DB
conn = sqlite3.connect("customer_data.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    amount_spent REAL,
    transaction_date TEXT
)
""")

# Insert sample data
sample_data = [
    ('Alice', 120.50, '2024-12-01'),
    ('Bob', 95.00, '2024-12-03'),
    ('Alice', 89.90, '2025-01-10'),
    ('Charlie', 150.00, '2025-02-14'),
    ('Bob', 60.00, '2025-03-01'),
    ('Diana', 200.00, '2025-03-05'),
    ('Charlie', 130.00, '2025-04-01'),
    ('Eve', 220.00, '2025-04-10'),
    ('Eve', 80.00, '2025-04-15')
]
cursor.executemany("INSERT INTO transactions (customer_name, amount_spent, transaction_date) VALUES (?, ?, ?)", sample_data)
conn.commit()

# Query 1: Total spent by customer
query1 = """
SELECT customer_name, SUM(amount_spent) AS total_spent 
FROM transactions GROUP BY customer_name
"""
df1 = pd.read_sql_query(query1, conn)
print("\n💳 Total Spent by Customer:\n", df1)

# Query 2: Average spending per transaction
query2 = "SELECT customer_name, AVG(amount_spent) AS avg_spent FROM transactions GROUP BY customer_name"
df2 = pd.read_sql_query(query2, conn)
print("\n📈 Average Spending per Transaction:\n", df2)

# Query 3: Most recent transaction per customer
query3 = """
SELECT customer_name, MAX(transaction_date) AS last_transaction 
FROM transactions GROUP BY customer_name
"""
df3 = pd.read_sql_query(query3, conn)
print("\n🕒 Last Transaction Date per Customer:\n", df3)

# Query 4: Total spending across all customers
query4 = "SELECT SUM(amount_spent) AS total_revenue FROM transactions"
df4 = pd.read_sql_query(query4, conn)
print("\n🧾 Total Revenue from All Customers:\n", df4)

# Plot 1: Total spending by customer (bar chart)
df1.plot(kind='bar', x='customer_name', y='total_spent', color='teal', title="Total Spending by Customer", legend=False)
plt.ylabel("Total Spent")
plt.tight_layout()
plt.savefig("customer_spent_bar.png")
plt.show()

# Plot 2: Average spend per customer (bar chart)
df2.plot(kind='bar', x='customer_name', y='avg_spent', color='purple', title="Average Spend per Customer", legend=False)
plt.ylabel("Avg. Spend")
plt.tight_layout()
plt.savefig("customer_avg_spend.png")
plt.show()

# Plot 3: Pie chart of customer spending distribution
plt.figure(figsize=(6, 6))
plt.pie(df1['total_spent'], labels=df1['customer_name'], autopct='%1.1f%%', startangle=90)
plt.title("Spending Distribution")
plt.savefig("customer_spending_pie.png")
plt.show()

# Plot 4: Line plot of cumulative spending over time (aggregated)
query5 = """
SELECT transaction_date, SUM(amount_spent) as daily_total
FROM transactions GROUP BY transaction_date ORDER BY transaction_date
"""
df5 = pd.read_sql_query(query5, conn)
df5['transaction_date'] = pd.to_datetime(df5['transaction_date'])

plt.figure(figsize=(8, 4))
plt.plot(df5['transaction_date'], df5['daily_total'], marker='o', color='darkorange')
plt.title("Daily Spending Over Time")
plt.xlabel("Date")
plt.ylabel("Amount Spent")
plt.grid(True)
plt.tight_layout()
plt.savefig("daily_spending_line.png")
plt.show()

conn.close()
