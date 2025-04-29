import os
import json
import google.generativeai as genai
from insights.business_insights_agent import BusinessInsightsAgent
from insights.sql_generation_agent import SQLGenerationAgent
from insights.business_head_agent import BusinessHeadAgent  # <-- Add this import

class InsightsService:
    def __init__(
        self,
        business_insights_agent: BusinessInsightsAgent,
        sql_generation_agent: SQLGenerationAgent,
        business_head_agent: BusinessHeadAgent  # <-- Add this parameter
    ):
        self.prompt_file = "prompt.md"
        self.business_insights_agent = business_insights_agent
        self.sql_generation_agent = sql_generation_agent
        self.business_head_agent = business_head_agent  # <-- Store the agent
        genai.configure(api_key="AIzaSyAlUonPo28IYiA3z5OhQy97pS3pEJoItvU")
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def get_insights(self, prompt: str, elaboration:str) -> str:
        """
        Generates insights based on the provided prompt.
        Args:
            prompt: The prompt to generate insights from.
        Returns:
            A string containing the generated insights.
        """
        sql_generator_text = self.sql_generation_agent.generate_sql(elaboration)
        
        # Extract JSON from markdown code block
        if sql_generator_text.startswith("```json"):
            json_str = sql_generator_text.strip().split('\n', 1)[1]
            json_str = json_str.rsplit('```', 1)[0]
        else:
            json_str = sql_generator_text

        sql_json = json.loads(json_str)
        print(sql_json)
        return self.business_insights_agent.analyze(sql_json["sql"], prompt, gcs_bucket="data_pulled")

    def elaborate_business_head_query(self, user_query: str) -> str:
        """
        Uses the BusinessHeadAgent to elaborate a business head query.
        """
        elaboration = self.business_head_agent.elaborate_query(user_query)
        return {
            "prompt": user_query,
            "elaboration": elaboration.replace("markdown\n", "").replace("```", ""),
        }

    # def read_prompt_file(self) -> str:
    #     """
    #     Reads the content of the prompt.md file.
        
    #     Returns:
    #         str: Content of the prompt file
    #     """
    #     file_path = os.path.join(os.path.dirname(__file__), self.prompt_file)
    #     try:
    #         with open(file_path, 'r') as file:
    #             return file.read().strip()
    #     except FileNotFoundError:
    #         raise FileNotFoundError(f"Prompt file not found at {file_path}")

    # def generate_sql(self, enhanced_prompt: str = None) -> str:
    #     """
    #     Generates a SQL query based on the enhanced prompt.

    #     Args:
    #         enhanced_prompt: The prompt enhanced with schema information.
    #                        If None, reads from prompt.md file.

    #     Returns:
    #         A SQL query string.
    #     """
    #     if enhanced_prompt is None:
    #         enhanced_prompt = self.read_prompt_file()
        
    #     generate_sql_from_prompt = self.generate_sql_from_prompt(enhanced_prompt)

    #     return generate_sql_from_prompt

    # def generate_sql_from_prompt(self, prompt: str) -> str:
    #     """
    #     Generates a SQL query based on the provided prompt.

    #     Args:
    #         prompt: The prompt to generate SQL from.

    #     Returns:
    #         A SQL query string.
    #     """
    #     response = self.model.generate_content(prompt)
    #     return response.text
