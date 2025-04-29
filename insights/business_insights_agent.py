import os
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import google.generativeai as genai
import uuid
from google.cloud import storage

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
        if isinstance(df, (pd.DataFrame, pd.Series)):
            sample = df.head(5).to_markdown(index=False)
        else:
            sample = str(df.head(5))
        prompt = f"""
You are a data scientist. Given a user question and a pandas DataFrame named 'df', generate Python code (no explanation) to extract data that answers the question.

User Question: "{question}"

DataFrame columns: {list(df.columns)}

Sample Data:
{sample}

Use only pandas code, and use the variable 'df' as the input DataFrame. Output should be stored in a variable named 'insight_df'. Output should not contain any markdown or code blocks.
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
        if isinstance(df, pd.DataFrame):
            sample = df.head(5).to_markdown(index=False)
        elif isinstance(df, pd.Series):
            sample = df.head(5).to_markdown(index=False)
        else:
            sample = str(df)
        prompt = f"""
You're a business analyst. The user asked:

"{question}"

Here's the relevant extracted data:

{sample}

Provide a concise natural language insight.
"""
        response = self.llm.generate_content(prompt)
        return response.text.strip()

    def upload_dataframe_to_gcs(self, df, bucket_name, prefix="insight_failures"):
        import uuid
        from google.cloud import storage
        from datetime import timedelta

        if not isinstance(df, (pd.DataFrame, pd.Series)) or df.empty:
            return None
        if isinstance(df, pd.Series):
            df = df.to_frame()
            
        filename = f"{prefix}/{uuid.uuid4()}.csv"
        temp_path = f"/tmp/{uuid.uuid4()}.csv"
        df.to_csv(temp_path, index=False)
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_filename(temp_path)
        
        # Generate signed URL that expires in 7 days
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=7),
            method="GET"
        )
        
        return url

    def analyze(self, sql_query: str, user_question: str, gcs_bucket=None):
        # Step 1: Dry Run
        if not self.dry_run_sql(sql_query):
            return {
                "success": False,
                "error": "Invalid SQL query.",
                "sql_query": sql_query
            }

        # Step 2: Run SQL
        df = self.run_sql_query(sql_query)
        gcs_url = None
        if gcs_bucket:
            gcs_url = self.upload_dataframe_to_gcs(df, gcs_bucket)

        if df.empty:
            return {
                "success": False,
                "error": "Query returned no data.",
                "sql_query": sql_query,
                "gcs_url": gcs_url
            }

        # Step 3: Generate and execute pandas code
        pandas_code = self.generate_pandas_code(user_question, df)
        print("🔧 Generated Pandas Code:\n", pandas_code)
        try:
            insight_df = self.execute_pandas_code(pandas_code, df)
        except Exception as e:
            return {
                "success": False,
                "error": f"Pandas code execution failed: {e}",
                "pandas_code": pandas_code,
                "sql_query": sql_query,
                "gcs_url": gcs_url
            }
        try:
            # Step 4: Generate human insight
            insight_text = self.generate_natural_language_insight(insight_df, user_question)

            # Handle both DataFrame and Series for JSON serialization
            if isinstance(insight_df, pd.DataFrame):
                insight_records = insight_df.to_dict(orient="records")
            elif isinstance(insight_df, pd.Series):
                insight_records = insight_df.reset_index().to_dict(orient="records")
            else:
                insight_records = [{"value": insight_df}]

            return {
                "success": True,
                "gcs_url": gcs_url,
                "insight": insight_text,
                "sql_query": sql_query,
                "pandas_code": pandas_code
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Insight generation failed: {e}",
                "pandas_code": pandas_code,
                "sql_query": sql_query,
                "gcs_url": gcs_url
            }
