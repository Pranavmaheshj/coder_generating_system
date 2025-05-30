import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CodeGenerator:
    def __init__(self):
        self.api_token = os.getenv("HF_API_TOKEN")
        if not self.api_token:
            raise ValueError("Add your Hugging Face API token to the .env file")
        
        self.api_url = "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-Instruct-hf"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def generate(self, prompt, language="python"):
        full_prompt = f"Write {language} code for: {prompt}\n```{language}\n"

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "inputs": full_prompt,
                    "parameters": {"max_new_tokens": 256}
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            # Extract generated text safely
            generated = result[0]["generated_text"]
            # Trim prompt and remove code block markers
            cleaned = generated[len(full_prompt):].split("```")[0].strip()
            return cleaned

        except requests.exceptions.RequestException as req_err:
            return f"Request Error: {req_err}"
        except KeyError:
            return f"Unexpected response format: {response.json()}"
        except Exception as e:
            return f"Error: {str(e)}"

# Example usage:
# generator = CodeGenerator()
# print(generator.generate("a function that checks if a number is prime", language="python"))
