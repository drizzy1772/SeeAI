



from google import genai
from agent_evals.models import Case
import json
from google.genai import types

class SyntheticGenerator:
    def __init__(self, model: str = "gemini-3.5-flash"):
        self.model = model
        self.client = genai.Client()

    def generate(self, topic: str, count: int = 3) -> list[Case]:
        system_promt = f"""You are an expert AI Quality Assurance Engineer. 
Your task is to generate {count} diverse and realistic test cases to evaluate an AI agent on the following topic: "{topic}".

Each test case should test different edge cases, user intents, or complexities within the topic.

You must return the result STRICTLY as a JSON array of objects. Do not include any markdown formatting (like ```json), introduction, or conclusion. Just the raw JSON array.

Each object in the array must contain exactly these three keys:
- "name": A short, descriptive title for the test case (e.g., "Round-trip with specific dates").
- "input": The simulated user message or query.
- "expected_output": A description of the ideal agent response or the exact criteria the response must meet."""
        try:
            response = self.client.models.generate_content(
            model = self.model,
            contents = f"Generate {count} test cases anout: {topic}",
            config = types.GenerateContentConfig(
                system_instruction =system_promt,
                response_mime_type="application/json",
                )
            )
            result = json.loads(response.text)
        except Exception as e:
            result = []
        #if not internet our program making a result = [] an empty list    
        cases = []
        for item in result:
            case = Case(name=item["name"], input=item["input"], expected_output=item["expected_output"])
            cases.append(case)
        return cases