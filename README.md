# AI Code Reviewer

An AI-powered code reviewer that automatically analyzes GitHub pull requests and provides feedback using the Qwen/Qwen3-235B-A22B-fp8-tput model from Together.ai.

## Features

- Automatically listens to GitHub pull/merge request events
- Fetches full changed files (not just diffs)
- Uses the Qwen/Qwen3-235B-A22B-fp8-tput LLM from Together.ai for analysis
- Posts inline or summary suggestions
- Modular architecture for easy swapping of code platforms and LLMs

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   TOGETHER_API_KEY=your_together_api_key_here
   GITHUB_TOKEN=your_github_token_here
   ```

## Usage

### Running as a Server

Start the server to listen for GitHub webhook events:

```
python main.py
```

The server will run on port 5000 by default.

### Manual Review

You can also manually trigger a review for a specific pull request:

```
python main.py <pull_request_number>
```

For example, to review PR #5:

```
python main.py 5
```

### Setting Up GitHub Webhooks

1. Go to your GitHub repository settings
2. Navigate to "Webhooks" and click "Add webhook"
3. Set the Payload URL to your server URL (e.g., `http://your-server.com/webhook`)
4. Set the Content type to `application/json`
5. Select "Let me select individual events" and choose "Pull requests"
6. Click "Add webhook"

## Project Structure

```
/code_platforms/
  github.py             # GitHub implementation
  interface.py          # Abstract interface (for GitLab later)
/llm_client/
  together_client.py    # Qwen model integration
  base.py               # Abstract interface
/review_engine/
  reviewer.py           # Prompt builder, response parser
/webhooks/
  github_webhook.py     # Handles GitHub webhook events
/config/
  settings.py           # Read env vars, model/repo configs
/main.py                # Entry point
```

## Target Repository

The code reviewer is currently configured to work with the repository:
`mohammedImad10/testing_framework`

To change the target repository, modify the `TARGET_REPO` variable in `webhooks/github_webhook.py`.
