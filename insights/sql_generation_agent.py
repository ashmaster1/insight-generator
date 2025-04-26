import google.generativeai as genai
import os
class SQLGenerationAgent:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.llm = genai.GenerativeModel('gemini-1.5-flash')  # Use 'gemini-1.5-pro' if needed

    def read_context(self) -> str:
        """
        Reads the content of a file.
        Args:
            file_path: The path to the file.
        Returns:
            A string containing the file's content.
        """
        file_path = os.path.join(os.path.dirname(__file__), "agent_training2.md")
        with open(file_path, 'r') as file:
            return file.read().strip()

    def generate_sql(self, prompt: str) -> str:
        """
        Generates SQL query based on the provided prompt.
        Args:
            prompt: The prompt to generate SQL from.
        Returns:
            A string containing the generated SQL query.
        """
        context = self.read_context()
        # Insert the user prompt into the context at {user_conversation}
        if "{user_conversation}" in context:
            combined_prompt = context.replace("{user_conversation}", prompt)
        else:
            combined_prompt = context + f"\nUser Conversation: {prompt}"
        response = self.llm.generate_content(combined_prompt)
        return response.text