import os
import streamlit as st
import pyodbc
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAI API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the function to get a response from Google Gemini Model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the SQL Server database
def read_sql_query(sql):
    # Configure your SQL Server connection here
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-13019E2\SQLEXPRESS;"
        "Database=EMPLOYEES;"
        "UID=sa;"
        "PWD=pa55w0rd;"
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# prompt
prompt = [
    """
    Act as an expert in converting questions to SQL query
    The SQL database has the name EMPLOYEES and has the following columns - NAME, EMPLOYEEID, 
    AGE and EXPERIENCE. For example:
    - Example 1: "How many entries of records are present?" would yield the SQL command:
      SELECT COUNT(*) FROM EMPLOYEES;
    - Example 2: "Tell me all the employees with 2+ years of experience?" would yield:
      SELECT * FROM EMPLOYEES WHERE EXPERIENCE >= 2;
    Also, please ensure the output SQL code does not contain ``` at the beginning or end, nor the word "sql" in it.
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    sql_query = get_gemini_response(question, prompt)
    print(sql_query)  # Generate SQL query
    response = read_sql_query(sql_query)
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)
