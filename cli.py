# cli.py
import sys
import click
from chat_system import ChatSystem
from config import Config
from pathlib import Path
import time

@click.group()
def cli():
    """GitHub-based chat system"""
    pass

@click.command()
@click.option('--token', help='GitHub API token')
@click.option('--owner', help='Repository owner')
@click.option('--repo', help='Repository name')
@click.option('--cache/--no-cache', default=True, help='Use cached messages')
def show(token, owner, repo, cache):
    """Display all messages"""
    try:
        chat = ChatSystem(token, owner, repo)
        click.echo(chat.format_messages(use_cache=cache))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@click.command()
@click.option('--filename', help='Optional custom filename (without .txt)')
@click.argument('message')
def send(message, filename):
    """Send a new message"""
    try:
        chat = ChatSystem()
        if not filename:
            filename = f"msg_{int(time.time())}"
        
        # Ensure messages directory exists
        messages_dir = Path('messages')
        messages_dir.mkdir(exist_ok=True)
        
        # Write message to file
        filepath = messages_dir / f"{filename}.txt"
        filepath.write_text(message)
        
        click.echo(f"Message saved to {filepath}")
        click.echo("Remember to commit and push your changes!")
    except Exception as e:
        click.echo(f"Error sending message: {e}", err=True)
        sys.exit(1)

@click.command()
@click.argument('key')
@click.argument('value')
def config(key, value):
    """Set a configuration value"""
    try:
        conf = Config()
        conf.set(key, value)
        click.echo(f"Set {key} to {value}")
    except Exception as e:
        click.echo(f"Error setting config: {e}", err=True)
        sys.exit(1)

@click.command()
def show_config():
    """Show current configuration"""
    try:
        conf = Config()
        for key, value in conf.settings.items():
            click.echo(f"{key}: {value}")
    except Exception as e:
        click.echo(f"Error reading config: {e}", err=True)
        sys.exit(1)

@click.command()
def update_cache():
    """Update the local message cache"""
    try:
        chat = ChatSystem()
        chat.update_cache()
        click.echo("Cache updated successfully!")
    except Exception as e:
        click.echo(f"Error updating cache: {e}", err=True)
        sys.exit(1)

cli.add_command(show)
cli.add_command(send)
cli.add_command(config)
cli.add_command(show_config)
cli.add_command(update_cache)

if __name__ == '__main__':
    cli()
