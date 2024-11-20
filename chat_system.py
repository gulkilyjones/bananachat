# chat_system.py
from datetime import datetime
from pathlib import Path
from config import Config
from cache_manager import CacheManager
from github_client import GitHubClient
from logger import logger

class ChatSystem:
    def __init__(self, token=None, owner=None, repo=None):
        self.config = Config()
        
        # Use provided values or fall back to config
        self.token = token or self.config.get('github_token')
        self.owner = owner or self.config.get('owner')
        self.repo = repo or self.config.get('repo')
        
        self.cache = CacheManager(self.config.get('cache_dir'))
        self.github = GitHubClient(self.token, self.owner, self.repo)

    def update_cache(self):
        """Update local cache from GitHub"""
        try:
            messages = self.github.get_messages()
            
            # Clear existing cache
            self.cache.clear()
            
            # Save messages and metadata
            metadata = []
            for msg in messages:
                self.cache.save_message(msg['filename'], msg['content'])
                metadata.append({
                    'filename': msg['filename'],
                    'author': msg['author'],
                    'date': msg['date'].isoformat(),
                    'commit_hash': msg.get('commit_hash')
                })
            
            self.cache.save_metadata(metadata)
            
        except Exception as e:
            logger.error(f"Error updating cache: {e}")
            raise

    def format_messages(self, use_cache=True):
        """Format messages for display"""
        try:
            messages = self.cache.get_messages() if use_cache else self.github.get_messages()
            
            if not messages:
                return "No messages found."
                
            # Sort messages by date
            messages.sort(key=lambda x: x['date'])
            
            # Format each message
            formatted = []
            for msg in messages:
                formatted.append(
                    f"[{msg['date'].strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{msg['author']} ({msg['filename']}): {msg['content']}"
                )
                
            return '\n'.join(formatted)
            
        except Exception as e:
            logger.error(f"Error formatting messages: {e}")
            return f"Error: Unable to format messages: {e}"
