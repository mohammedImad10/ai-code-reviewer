import requests
import os

class GitHub:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com/'

    def fetch_pull_request_files(self, repo, pull_number):
        url = f'{self.base_url}repos/{repo}/pulls/{pull_number}/files'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def fetch_file_content(self, repo, file_path, ref):
        url = f'{self.base_url}repos/{repo}/contents/{file_path}?ref={ref}'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()
        
    def post_comment(self, repo, pull_number, comment, path=None, line=None):
        """Post a comment to a pull request, either as a general comment or as a review comment on a specific line."""
        if path and line:
            # Post a review comment on a specific line
            url = f'{self.base_url}repos/{repo}/pulls/{pull_number}/comments'
            payload = {
                "body": comment,
                "commit_id": self.get_latest_commit_id(repo, pull_number),
                "path": path,
                "line": line
            }
        else:
            # Post a general comment
            url = f'{self.base_url}repos/{repo}/issues/{pull_number}/comments'
            payload = {"body": comment}
            
        headers = {'Authorization': f'token {self.token}'}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
        
    def get_latest_commit_id(self, repo, pull_number):
        """Get the latest commit ID for a pull request."""
        url = f'{self.base_url}repos/{repo}/pulls/{pull_number}/commits'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        commits = response.json()
        if commits:
            return commits[-1]['sha']
        return None
