import sys
import click
from config import Config

SUPPORTED_KEYS = ['github_token', 'repo_owner', 'repo_name', 'cache_enabled']

@click.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
def config(key, value):
    """Set a configuration value"""
    if not key or not value:
        click.echo("Supported configuration keys:")
        for k in SUPPORTED_KEYS:
            click.echo(f"  {k}")
        click.echo("\nUsage: cli config KEY VALUE")
        return

    if key not in SUPPORTED_KEYS:
        click.echo(f"Error: Unsupported configuration key: {key}")
        click.echo("Run 'cli config' to see supported keys")
        sys.exit(1)

    try:
        conf = Config()
        conf.set(key, value)
        click.echo(f"Set {key} to {value}")
    except Exception as e:
        click.echo(f"Error setting config: {e}", err=True)
        sys.exit(1)

@click.command(name='show-config')
def show_config():
    """Show current configuration"""
    try:
        conf = Config()
        if not conf.settings:
            click.echo("No configuration values set")
            click.echo("\nSupported keys:")
            for key in SUPPORTED_KEYS:
                click.echo(f"  {key}")
            return

        for key, value in conf.settings.items():
            click.echo(f"{key}: {value}")
    except Exception as e:
        click.echo(f"Error reading config: {e}", err=True)
        sys.exit(1)
