import click
from commands.show import show
from commands.send import send
from commands.config import config, show_config
from commands.cache import update_cache

@click.group()
def cli():
    """GitHub-based chat system"""
    pass

cli.add_command(show)
cli.add_command(send)
cli.add_command(config)
cli.add_command(show_config)
cli.add_command(update_cache)

if __name__ == '__main__':
    cli()
