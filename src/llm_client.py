import json
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "local").strip().lower()

    def is_enabled(self):
        return self.provider in {"openai", "azure"}

    def generate(self, prompt):
        if self.provider == "openai":
            return self._generate_openai(prompt)
        if self.provider == "azure":
            return self._generate_azure(prompt)
        raise RuntimeError("Local mode does not call a remote LLM.")

    def _generate_openai(self, prompt):
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a senior QA engineer. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
        )
        return self._parse_json(response.choices[0].message.content or "[]")

    def _generate_azure(self, prompt):
        from openai import AzureOpenAI
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        if not all([api_key, endpoint, deployment]):
            raise RuntimeError("Azure OpenAI configuration is incomplete.")
        client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=version)
        response = client.chat.completions.create(
            model=deployment,
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a senior QA engineer. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
        )
        return self._parse_json(response.choices[0].message.content or "[]")

    @staticmethod
    def _parse_json(content):
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()
        data = json.loads(cleaned)
        if isinstance(data, dict) and "test_cases" in data:
            data = data["test_cases"]
        if not isinstance(data, list):
            raise ValueError("LLM response must be a JSON array.")
        return data
