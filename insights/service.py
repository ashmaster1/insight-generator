import os
import google.generativeai as genai

class InsightsService:
    def __init__(self):
        self.prompt_file = "prompt.md"
        # Configure the library with your API key
        genai.configure(api_key="AIzaSyAlUonPo28IYiA3z5OhQy97pS3pEJoItvU")
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def read_prompt_file(self) -> str:
        """
        Reads the content of the prompt.md file.
        
        Returns:
            str: Content of the prompt file
        """
        file_path = os.path.join(os.path.dirname(__file__), self.prompt_file)
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found at {file_path}")

    def generate_sql(self, enhanced_prompt: str = None) -> str:
        """
        Generates a SQL query based on the enhanced prompt.

        Args:
            enhanced_prompt: The prompt enhanced with schema information.
                           If None, reads from prompt.md file.

        Returns:
            A SQL query string.
        """
        if enhanced_prompt is None:
            enhanced_prompt = self.read_prompt_file()
        
        generate_sql_from_prompt = self.generate_sql_from_prompt(enhanced_prompt)

        return generate_sql_from_prompt

    def generate_sql_from_prompt(self, prompt: str) -> str:
        """
        Generates a SQL query based on the provided prompt.

        Args:
            prompt: The prompt to generate SQL from.

        Returns:
            A SQL query string.
        """
        response = self.model.generate_content(prompt)
        return response.text
