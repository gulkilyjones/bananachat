# github_client.py
import requests
from datetime import datetime
from logger import logger

class GitHubClient:
    def __init__(self, token, owner, repo):
        self.owner = owner
        self.repo = repo
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        })

    def get_messages(self):
        """Fetch all messages from the repository"""
        try:
            url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/messages'
            response = self.session.get(url)
            response.raise_for_status()
            contents = response.json()
            
            messages = []
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.txt'):
                    message = self._process_message_file(item)
                    if message:
                        messages.append(message)
            return messages
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")
            raise

    def _process_message_file(self, item):
        """Process a single message file"""
        try:
            # Get file content
            response = self.session.get(item['download_url'])
            response.raise_for_status()
            content = response.text.strip()
            
            # Get commit info
            commits_url = f'https://api.github.com/repos/{self.owner}/{self.repo}/commits'
            commits_response = self.session.get(commits_url, params={'path': f"messages/{item['name']}"})
            commits_response.raise_for_status()
            commits = commits_response.json()
            
            if commits:
                author = commits[0]['commit']['author']['name']
                date = datetime.strptime(
                    commits[0]['commit']['author']['date'],
                    '%Y-%m-%dT%H:%M:%SZ'
                )
                commit_hash = commits[0]['sha']
            else:
                author = "unknown"
                date = datetime.now()
                commit_hash = None
            
            return {
                'filename': item['name'],
                'content': content,
                'author': author,
                'date': date,
                'commit_hash': commit_hash
            }
        except Exception as e:
            logger.error(f"Error processing message {item['name']}: {e}")
            return None
