import os
import google.generativeai as genai

class BusinessHeadAgent:
    def __init__(self, gemini_api_key: str, prompt_path: str = None):
        genai.configure(api_key=gemini_api_key)
        self.llm = genai.GenerativeModel('gemini-1.5-flash')
        if prompt_path is None:
            prompt_path = os.path.join(os.path.dirname(__file__), "business_head.md")
        self.prompt_path = prompt_path
        self.prompt_template = self._read_prompt_file()

    def _read_prompt_file(self) -> str:
        with open(self.prompt_path, "r") as f:
            return f.read()

    def elaborate_query(self, user_query: str) -> str:
        prompt = f"""
{self.prompt_template}

---
**Query**: "{user_query}"

Follow the instructions above and output the required context, raw data requirements, and instruction in markdown format.
"""
        response = self.llm.generate_content(prompt)
        return response.text.strip()