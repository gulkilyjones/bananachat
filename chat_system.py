# chat_system.py
import os
import sys
import time
import base64
import logging
from datetime import datetime
from pathlib import Path
import requests
import click
from ratelimit import limits, sleep_and_retry

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class GitHubError(Exception):
    """Custom exception for GitHub API errors"""
    pass

class RateLimitError(GitHubError):
    """Raised when GitHub API rate limit is hit"""
    pass

class ChatSystem:
    def __init__(self, token, owner, repo):
        self.owner = owner
        self.repo = repo
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.local_dir = Path('messages')
        self.local_dir.mkdir(exist_ok=True)
        
    def _handle_response(self, response, context="API call"):
        """Handle API response and common errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                remaining = response.headers.get('X-RateLimit-Remaining', '0')
                if remaining == '0':
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(reset_time - time.time(), 0)
                    raise RateLimitError(
                        f"Rate limit exceeded. Resets in {wait_time:.0f} seconds"
                    )
            elif response.status_code == 404:
                raise GitHubError(f"Resource not found: {context}")
            raise GitHubError(f"GitHub API error: {e}")
        except requests.exceptions.RequestException as e:
            raise GitHubError(f"Network error: {e}")
        except ValueError as e:
            raise GitHubError(f"Invalid JSON response: {e}")

    @sleep_and_retry
    @limits(calls=30, period=60)  # GitHub API rate limit
    def get_forks(self):
        """Get all forks of the repository with rate limiting"""
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/forks'
        response = self.session.get(url)
        return self._handle_response(response, "getting forks")

    @sleep_and_retry
    @limits(calls=30, period=60)
    def get_messages_from_fork(self, fork_owner):
        """Fetch messages directly from a fork using the GitHub API"""
        try:
            # Get contents of messages directory
            url = f'https://api.github.com/repos/{fork_owner}/{self.repo}/contents/messages'
            response = self.session.get(url)
            contents = self._handle_response(response, f"getting messages from {fork_owner}")
            
            messages = []
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.txt'):
                    try:
                        # Get file content
                        response = self.session.get(item['download_url'])
                        response.raise_for_status()
                        content = response.text.strip()
                        
                        # Parse filename for metadata
                        filename = Path(item['name'])
                        timestamp, author = filename.stem.split('_', 1)
                        
                        messages.append({
                            'timestamp': timestamp,
                            'author': author,
                            'content': content,
                            'source': fork_owner
                        })
                    except Exception as e:
                        logger.error(f"Error fetching message {item['name']} from {fork_owner}: {e}")
                        continue
                        
            return messages
            
        except GitHubError as e:
            logger.error(f"Error accessing fork {fork_owner}: {e}")
            return []

    async def sync_messages(self):
        """Sync messages from all forks"""
        try:
            forks = self.get_forks()
            all_messages = []
            
            # Get messages from main repo
            main_messages = self.get_messages_from_fork(self.owner)
            all_messages.extend(main_messages)
            
            # Get messages from each fork
            for fork in forks:
                fork_owner = fork['owner']['login']
                try:
                    fork_messages = self.get_messages_from_fork(fork_owner)
                    all_messages.extend(fork_messages)
                except Exception as e:
                    logger.error(f"Error processing fork {fork_owner}: {e}")
                    continue
            
            # Save messages locally
            for msg in all_messages:
                filename = f"{msg['timestamp']}_{msg['author']}.txt"
                filepath = self.local_dir / filename
                if not filepath.exists():
                    try:
                        filepath.write_text(msg['content'])
                        logger.info(f"Saved new message from {msg['author']} ({msg['source']})")
                    except Exception as e:
                        logger.error(f"Error saving message to {filename}: {e}")
                        
            return all_messages
            
        except Exception as e:
            logger.error(f"Error during message sync: {e}")
            raise

    def add_message(self, content, author):
        """Add a new message locally"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{author}.txt"
            filepath = self.local_dir / filename
            
            filepath.write_text(content)
            logger.info(f"Added new message from {author}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            raise GitHubError(f"Failed to add message: {e}")

    def format_messages(self):
        """Format all messages for display"""
        messages = []
        try:
            for msg_file in sorted(self.local_dir.glob('*.txt')):
                try:
                    timestamp, author = msg_file.stem.split('_', 1)
                    content = msg_file.read_text().strip()
                    dt = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
                    messages.append(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')}] {author}: {content}")
                except Exception as e:
                    logger.error(f"Error reading message {msg_file}: {e}")
                    continue
                    
            return '\n'.join(messages)
            
        except Exception as e:
            logger.error(f"Error formatting messages: {e}")
            return "Error: Unable to format messages"

# CLI Interface
@click.group()
def cli():
    """Simple GitHub-based chat system"""
    pass

@cli.command()
@click.option('--token', envvar='GITHUB_TOKEN', required=True, help='GitHub API token')
@click.option('--owner', required=True, help='Repository owner')
@click.option('--repo', required=True, help='Repository name')
def sync(token, owner, repo):
    """Sync messages from all forks"""
    try:
        chat = ChatSystem(token, owner, repo)
        click.echo("Syncing messages...")
        chat.sync_messages()
        click.echo("Sync complete!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--token', envvar='GITHUB_TOKEN', required=True, help='GitHub API token')
@click.option('--owner', required=True, help='Repository owner')
@click.option('--repo', required=True, help='Repository name')
@click.option('--author', required=True, help='Message author')
@click.argument('message')
def send(token, owner, repo, author, message):
    """Send a new message"""
    try:
        chat = ChatSystem(token, owner, repo)
        chat.add_message(message, author)
        click.echo("Message sent!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--token', envvar='GITHUB_TOKEN', required=True, help='GitHub API token')
@click.option('--owner', required=True, help='Repository owner')
@click.option('--repo', required=True, help='Repository name')
def show(token, owner, repo):
    """Display all messages"""
    try:
        chat = ChatSystem(token, owner, repo)
        click.echo(chat.format_messages())
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
