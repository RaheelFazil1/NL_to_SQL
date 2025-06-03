import sys
from gemini_utils import generate_sql_query, explain_results
from db_utils import connect_to_db, execute_sql_query

def sanitize_sql(sql_query):
    """Basic sanitization to ensure only SELECT queries."""
    if not sql_query.lower().strip().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    return sql_query

def format_sql_for_execution(sql_query):
    """Replace placeholders for parameterized queries."""
    return sql_query  # For now, assuming Gemini doesn't inject values directly

def get_user_input():
    print("\nEnter your question (type 'exit' to quit):")
    user_input = input(">> ").strip()
    if user_input.lower() == "exit":
        print("[INFO] Exiting...")
        sys.exit()
    return user_input

def display_results(df, explanation):
    print("\n📊 Query Results:")
    print(df.to_string(index=False))
    print("\n📝 Explanation:")
    print(explanation)

def main():
    conn = connect_to_db()
    if not conn:
        print("[❌ ERROR] Could not connect to database. Exiting.")
        return

    while True:
        user_question = get_user_input()
        print("[INFO] Translating query to SQL...")

        raw_sql = generate_sql_query(user_question, tbl_name='Test_TSSR')
        if not raw_sql:
            print("[❌ ERROR] Failed to generate valid SQL query.")
            continue

        print(f"[✅ INFO] Raw SQL: {raw_sql}")

        try:
            safe_sql = sanitize_sql(raw_sql)
        except ValueError as ve:
            print(f"[❌ ERROR] Invalid query type: {ve}")
            continue

        print("[INFO] Executing SQL query...")
        result_df = execute_sql_query(safe_sql, conn)
        if result_df is None or result_df.empty:
            print("[❌ ERROR] No results found or invalid query.")
            continue

        explanation = explain_results(result_df)
        display_results(result_df, explanation)

if __name__ == "__main__":
    main()