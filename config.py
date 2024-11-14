# config.py
import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_file = Path.home() / '.bananachat.json'
        self.defaults = {
            'github_token': '',
            'owner': '',
            'repo': '',
            'cache_dir': str(Path.home() / '.bananachat' / 'cache'),
            'messages_dir': 'messages'
        }
        self.settings = self.load_config()

    def load_config(self):
        """Load config from file or create with defaults"""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return {**self.defaults, **json.load(f)}
            except json.JSONDecodeError:
                return self.defaults
        return self.defaults

    def save_config(self):
        """Save current config to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key):
        """Get a config value, first checking env vars"""
        env_var = f'BANANACHAT_{key.upper()}'
        return os.getenv(env_var, self.settings.get(key, self.defaults.get(key)))

    def set(self, key, value):
        """Set a config value and save"""
        self.settings[key] = value
        self.save_config()
