
import os
import sys
import logging
from dotenv import load_dotenv
from webhooks.github_webhook import app, process_pull_request, TARGET_REPO

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('code_reviewer.log')
    ]
)

if __name__ == '__main__':
    # Check if we're running with arguments for manual review
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        # Manual review mode
        pull_number = int(sys.argv[1])
        logging.info(f"Manual review mode for PR #{pull_number}")
        process_pull_request(TARGET_REPO, pull_number)
    else:
        # Server mode
        logging.info("Starting AI Code Reviewer server...")
        logging.info(f"Target repository: {TARGET_REPO}")
        app.run(host='0.0.0.0', port=5000, debug=True)