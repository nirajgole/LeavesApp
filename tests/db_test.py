import pyodbc

server = 'N7\MSSQL'  # Use comma for port if specifying instance and port together

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    'DATABASE=Jomato;'
    'Trusted_Connection=yes;'
    # 'TrustServerCertificate=yes;' # Added for security handshake stability
)

print(f"Attempting to connect to {server}...")

try:
    # 1. Establish connection
    conn = pyodbc.connect(conn_str, timeout=60)
    cursor = conn.cursor()
    print("✅ Connection Successful!")

    # 2. Query an existing table (e.g., employees)
    # If you haven't created 'employees' yet, change this to any existing table name
    table_name = "restaurants"
    print(f"Querying top 5 rows from {table_name}...")

    cursor.execute(f"SELECT TOP 5 * FROM {table_name}")

    rows = cursor.fetchall()
    if not rows:
        print(f"Connected, but the table '{table_name}' is empty.")
    for row in rows:
        print(row)

    conn.close()

except pyodbc.OperationalError as e:
    print("\n❌ Connection Failed!")
    print(f"Error details: {e}")
    print("\n💡 Troubleshooting Tip: Ensure 'SQL Server Browser' service is running in SQL Configuration Manager if you use a named instance (like localhost\\SQLEXPRESS).")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")