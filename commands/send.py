import sys
import click
import time
from pathlib import Path
from chat_system import ChatSystem

@click.command()
@click.option('--filename', help='Optional custom filename (without .txt)')
@click.argument('message', required=False)
def send(message, filename):
    """Send a new message"""
    if not message:
        click.echo("Available options:")
        click.echo("  --filename TEXT  Optional custom filename (without .txt)")
        click.echo("\nUsage: cli send [OPTIONS] MESSAGE")
        return

    try:
        chat = ChatSystem()
        if not filename:
            filename = f"msg_{int(time.time())}"
        
        messages_dir = Path('messages')
        messages_dir.mkdir(exist_ok=True)
        
        filepath = messages_dir / f"{filename}.txt"
        filepath.write_text(message)
        
        click.echo(f"Message saved to {filepath}")
        click.echo("Remember to commit and push your changes!")
    except Exception as e:
        click.echo(f"Error sending message: {e}", err=True)
        sys.exit(1)
