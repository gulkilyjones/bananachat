import sys
import click
from chat_system import ChatSystem

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

