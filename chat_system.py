# chat_system.py
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import requests
import click
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('chat.log'),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger(__name__)


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

    def get_messages_from_repo(self):
        """Fetch messages directly from the repository"""
        try:
            # Get contents of messages directory
            url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/messages'
            response = self.session.get(url)
            response.raise_for_status()
            contents = response.json()

            messages = []
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.txt'):
                    try:
                        # Get file content
                        response = self.session.get(item['download_url'])
                        response.raise_for_status()
                        content = response.text.strip()

                        # Get file metadata from GitHub
                        file_info_url = f'https://api.github.com/repos/{self.owner}/{self.repo}/commits?path=messages/{item["name"]}'
                        commits_response = self.session.get(file_info_url)
                        commits_response.raise_for_status()
                        commits = commits_response.json()

                        if commits:
                            # Use the first commit's author and date
                            author = commits[0]['commit']['author']['name']
                            date = datetime.strptime(
                                commits[0]['commit']['author']['date'],
                                '%Y-%m-%dT%H:%M:%SZ')
                        else:
                            # Fallback to file name and current time
                            author = "unknown"
                            date = datetime.now()

                        messages.append({
                            'filename': item['name'],
                            'content': content,
                            'author': author,
                            'date': date
                        })

                    except Exception as e:
                        logger.error(
                            f"Error fetching message {item['name']}: {e}")
                        continue

            return messages

        except requests.exceptions.RequestException as e:
            logger.error(f"Error accessing repository: {e}")
            return []

    def format_messages(self):
        """Format messages for display"""
        try:
            messages = self.get_messages_from_repo()

            # Sort messages by date
            messages.sort(key=lambda x: x['date'])

            # Format each message
            formatted = []
            for msg in messages:
                formatted.append(
                    f"[{msg['date'].strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{msg['author']} ({msg['filename']}): {msg['content']}")

            return '\n'.join(formatted) if formatted else "No messages found."

        except Exception as e:
            logger.error(f"Error formatting messages: {e}")
            return f"Error: Unable to format messages: {e}"

    def add_message(self, content, filename=None):
        """Add a new message file"""
        try:
            if filename is None:
                # Generate a timestamp-based filename if none provided
                filename = f"msg_{int(time.time())}.txt"

            if not filename.endswith('.txt'):
                filename += '.txt'

            filepath = self.local_dir / filename
            filepath.write_text(content)
            logger.info(f"Added new message: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Error adding message: {e}")
            raise


@click.group()
def cli():
    """Simple GitHub-based chat system"""
    pass


@click.command()
@click.option('--token', required=True, help='GitHub API token')
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


@click.command()
@click.option('--token', required=True, help='GitHub API token')
@click.option('--owner', required=True, help='Repository owner')
@click.option('--repo', required=True, help='Repository name')
@click.option('--filename', help='Optional filename for the message')
@click.argument('content')
def send(token, owner, repo, filename, content):
    """Send a new message"""
    try:
        chat = ChatSystem(token, owner, repo)
        chat.add_message(content, filename)
        click.echo("Message sent!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


cli.add_command(show)
cli.add_command(send)

if __name__ == '__main__':
    cli()
