import together
from dotenv import load_dotenv
import os

load_dotenv()

class TogetherClient:
    def __init__(self):
        # Initialize the client with the API key from environment variables
        together.api_key = os.getenv('TOGETHER_API_KEY')

    def get_completion(self, prompt):
        response = together.Complete.create(
            model="Qwen/Qwen3-235B-A22B-fp8-tput",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.7
        )
        return response
