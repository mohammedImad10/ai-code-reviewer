from flask import Flask, request, jsonify
from code_platforms.github import GitHub
from review_engine.reviewer import Reviewer
from llm_client.together_client import TogetherClient
import base64
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Hardcoded repository for testing
TARGET_REPO = "mohammedImad10/testing_framework"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    logging.info(f"Received webhook: {data.get('action', 'unknown action')}")
    
    # Check if this is a pull request event
    if 'pull_request' in data and data.get('action') in ['opened', 'synchronize']:
        repo = data.get('repository', {}).get('full_name', TARGET_REPO)
        pull_number = data.get('number')
        
        if not pull_number:
            logging.error("Pull request number not found in webhook data")
            return jsonify({"error": "Pull request number not found"}), 400
            
        process_pull_request(repo, pull_number)
        return '', 204
    
    return jsonify({"message": "Event ignored"}), 200

@app.route('/review/<int:pull_number>', methods=['GET'])
def manual_review(pull_number):
    """Endpoint for manually triggering a review of a specific PR"""
    process_pull_request(TARGET_REPO, pull_number)
    return jsonify({"message": f"Review initiated for PR #{pull_number}"}), 200

def process_pull_request(repo, pull_number):
    """Process a pull request and generate code review comments"""
    logging.info(f"Processing PR #{pull_number} for repo {repo}")
    
    try:
        github = GitHub()
        files = github.fetch_pull_request_files(repo, pull_number)
        reviewer = Reviewer()
        llm_client = TogetherClient()
        
        if not files:
            logging.warning(f"No files found in PR #{pull_number}")
            github.post_comment(repo, pull_number, "No files found to review in this PR.")
            return
            
        logging.info(f"Found {len(files)} files to review")
        
        for file in files:
            file_path = file['filename']
            # Skip non-code files or files that are too large
            if not should_review_file(file_path, file.get('changes', 0)):
                continue
                
            ref = file.get('contents_url', '').split('?ref=')[-1] if 'contents_url' in file else 'main'
            
            try:
                file_content = github.fetch_file_content(repo, file_path, ref)
                
                # GitHub API returns content as base64 encoded
                if 'content' in file_content and file_content.get('encoding') == 'base64':
                    decoded_content = base64.b64decode(file_content['content']).decode('utf-8')
                    prompt = reviewer.construct_prompt(decoded_content)
                    
                    # Call the LLM for code review
                    response = llm_client.get_completion(prompt)
                    suggestions = reviewer.parse_response(response)
                    logging.info(f"Received response from LLM for {file_path}")
                    
                    # Post the review as a comment
                    if suggestions:
                        comment = f"### AI Code Review for `{file_path}`\n\n"
                        comment += "\n".join(suggestions)
                        github.post_comment(repo, pull_number, comment, file_path, None)
                        logging.info(f"Posted review for {file_path}")
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {str(e)}")
                continue
                
        # Post a summary comment
        github.post_comment(repo, pull_number, "✅ AI code review completed. See individual file comments for details.")
        
    except Exception as e:
        logging.error(f"Error processing PR #{pull_number}: {str(e)}")
        github = GitHub()
        github.post_comment(repo, pull_number, f"⚠️ Error during code review: {str(e)}")

def should_review_file(file_path, changes):
    """Determine if a file should be reviewed based on its extension and size"""
    # Skip files that are too large (more than 1000 lines changed)
    if changes > 1000:
        return False
        
    # Only review code files
    code_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', '.h', '.cs', '.go', '.rb', '.php']
    return any(file_path.endswith(ext) for ext in code_extensions)
