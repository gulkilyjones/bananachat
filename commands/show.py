import sys
import click
from chat_system import ChatSystem

@click.command()
@click.option('--token', help='GitHub API token')
@click.option('--owner', help='Repository owner')
@click.option('--repo', help='Repository name')
@click.option('--cache/--no-cache', default=True, help='Use cached messages')
def show(token, owner, repo, cache):
    """Display all messages"""
    if not any([token, owner, repo]):
        click.echo("Available options:")
        click.echo("  --token TEXT   GitHub API token")
        click.echo("  --owner TEXT   Repository owner")
        click.echo("  --repo TEXT    Repository name")
        click.echo("  --cache/--no-cache  Use cached messages (default: True)")
        return

    try:
        chat = ChatSystem(token, owner, repo)
        click.echo(chat.format_messages(use_cache=cache))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
