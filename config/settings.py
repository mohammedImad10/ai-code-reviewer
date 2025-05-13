import os
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
