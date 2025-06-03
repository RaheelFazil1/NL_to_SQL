import google.generativeai as genai
from config import GEMINI_API_KEY
import pandas as pd



genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel("gemini-1.5-flash")

# prompt = "who are you?"
# response = model.generate_content(prompt)
# print(response.text)


def generate_sql_query(natural_language, tbl_name):
    prompt = f"""
        You are a helpful assistant that translates natural language into SQL queries.
        The target database is a SQL Server table named {tbl_name}.
        These are the column names: ['site_id', 'latitude', 'longitude', 'site_name', 'site_location', 'site_type', 'tower_height']
        Don't return "SELECT * FROM {tbl_name}", unless you know what you're doing.
        If you use COUNT(*) then give alias also like: COUNT(*) as Number of.
        Only return the SQL query without any extra text.
        
        Natural Language Query:
        "{natural_language}"
        
        Generated SQL Query:
        """
    try:
        response = model.generate_content(prompt)
        sql_query = response.text.replace("sql", " ").replace("`", " ").strip().replace("\n", " ")
        return sql_query if sql_query.lower().startswith("select") else None
    except Exception as e:
        print(f"[Gemini API Error]: {e}")
        return None

# qry = 'show all sites of Residential Area'
# tbl = 'Test_TSSR'
# rs_sql = generate_sql_query(qry, tbl)
# print(rs_sql)

def explain_results(results_df):
    if results_df.empty:
        return "No data matched your query."

    sample_data = results_df.head(15).to_string()
    prompt = f"""
            Explain these results from a database query in simple English:
            {sample_data}

            Summary:
            """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Could not generate explanation due to error: {e}"


# data = {
#     'site_id': [1234, 1235, 1236, 1237, 1238],
#     'latitude': [32.2446, 32.251, 32.239, 32.247, 32.255],
#     'longitude': [74.0568, 74.062, 74.05, 74.058, 74.065],
#     'site_name': ['SBA1234', 'SBA1235', 'SBA1236', 'SBA1237', 'SBA1238'],
#     'site_location': ['Residential Area', 'Industrial Zone', 'Commercial Area', 'Rural Area', 'Suburban Area'],
#     'site_type': ['New Green Field', 'Existing Site', 'New Green Field', 'New Green Field', 'Existing Site'],
#     'tower_height': [30, 45, 25, 35, 40]
# }
#
# test_df = pd.DataFrame(data)
# # print(test_df)
#
# explain = explain_results(test_df)
# print(explain)
