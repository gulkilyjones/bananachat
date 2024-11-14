# cache_manager.py
import json
from datetime import datetime
from pathlib import Path
from logger import logger

class CacheManager:
    def __init__(self, cache_dir):
        self.cache_dir = Path(cache_dir)
        self.messages_cache = self.cache_dir / 'messages'
        self.metadata_cache = self.cache_dir / 'metadata'
        
        # Create cache directories
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.messages_cache.mkdir(exist_ok=True)
        self.metadata_cache.mkdir(exist_ok=True)

    def save_message(self, filename, content):
        """Save a message to cache"""
        try:
            cache_path = self.messages_cache / filename
            cache_path.write_text(content)
        except Exception as e:
            logger.error(f"Error saving message to cache: {e}")
            raise

    def save_metadata(self, metadata):
        """Save metadata index"""
        try:
            with open(self.metadata_cache / 'index.json', 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            with open(self.cache_dir / 'last_update', 'w') as f:
                f.write(datetime.now().isoformat())
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            raise

    def get_messages(self):
        """Get all cached messages with metadata"""
        try:
            if not (self.metadata_cache / 'index.json').exists():
                return []
                
            with open(self.metadata_cache / 'index.json') as f:
                metadata = json.load(f)
                
            messages = []
            for meta in metadata:
                msg_path = self.messages_cache / meta['filename']
                if msg_path.exists():
                    messages.append({
                        'filename': meta['filename'],
                        'content': msg_path.read_text(),
                        'author': meta['author'],
                        'date': datetime.fromisoformat(meta['date'])
                    })
            return messages
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return []

    def clear(self):
        """Clear the cache"""
        try:
            for file in self.messages_cache.glob('*.txt'):
                file.unlink()
            if (self.metadata_cache / 'index.json').exists():
                (self.metadata_cache / 'index.json').unlink()
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            raise
