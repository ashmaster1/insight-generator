import os
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import google.generativeai as genai

class BusinessInsightsAgent:
    def __init__(self, bq_project_id: str, gemini_api_key: str):
        self.bq_client = bigquery.Client(project=bq_project_id)
        genai.configure(api_key=gemini_api_key)
        self.llm = genai.GenerativeModel('gemini-1.5-flash')  # Use 'gemini-1.5-pro' if needed

    def dry_run_sql(self, query: str) -> bool:
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
        try:
            self.bq_client.query(query, job_config=job_config)
            return True
        except BadRequest as e:
            print("❌ SQL Dry Run Failed:", e)
            return False

    def run_sql_query(self, query: str) -> pd.DataFrame:
        df = self.bq_client.query(query).to_dataframe()
        return df

    def generate_pandas_code(self, question: str, df: pd.DataFrame) -> str:
        sample = df.head(5).to_markdown(index=False)
        prompt = f"""
You are a data scientist. Given a user question and a pandas DataFrame, generate Python code (no explanation) to extract data that answers the question.

User Question: "{question}"

DataFrame columns: {list(df.columns)}

Sample Data:
{sample}

Use only pandas code. Output should be stored in a variable named 'insight_df'. Output should not contain any markdown or code blocks.
"""
        response = self.llm.generate_content(prompt)
        code = response.text.strip()
        # Remove markdown code block formatting if present
        if code.startswith("```"):
            code = code.strip("`")
            code = code.split('\n', 1)[-1]  # Remove the first line (``` or ```python)
            if code.endswith("```"):
                code = code.rsplit('\n', 1)[0]
        return code.strip()

    def execute_pandas_code(self, code: str, df: pd.DataFrame) -> pd.DataFrame:
        print("🔧 Executing Pandas Code...")
        print("🔧 Code:\n", code)  # Debugging: Print the generated code
        local_vars = {'df': df.copy()}
        exec(code, {}, local_vars)
        return local_vars.get('insight_df', df)

    def generate_natural_language_insight(self, df: pd.DataFrame, question: str) -> str:
        sample = df.to_markdown(index=False)
        prompt = f"""
You're a business analyst. The user asked:

"{question}"

Here's the relevant extracted data:

{sample}

Provide a concise natural language insight.
"""
        response = self.llm.generate_content(prompt)
        return response.text.strip()

    def analyze(self, sql_query: str, user_question: str):
        # Step 1: Dry Run
        if not self.dry_run_sql(sql_query):
            return {"success": False, "error": "Invalid SQL query."}

        # Step 2: Run SQL
        df = self.run_sql_query(sql_query)
        if df.empty:
            return {"success": False, "error": "Query returned no data."}

        # Step 3: Generate and execute pandas code
        pandas_code = self.generate_pandas_code(user_question, df)
        print("🔧 Generated Pandas Code:\n", pandas_code)
        insight_df = self.execute_pandas_code(pandas_code, df)

        # Step 4: Generate human insight
        insight_text = self.generate_natural_language_insight(insight_df, user_question)

        # Handle both DataFrame and Series for JSON serialization
        if isinstance(insight_df, pd.Series):
            insight_records = insight_df.reset_index().to_dict(orient="records")
        else:
            insight_records = insight_df.to_dict(orient="records")

        return {
            "success": True,
            "dataframe": insight_records,
            "insight": insight_text,
            "pandas_code": pandas_code
        }
