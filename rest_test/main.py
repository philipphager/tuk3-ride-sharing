import click

from requester import open_yaml, run_requests


@click.group()
def cli():
    pass


@cli.command()
@click.option('--input', help='Path to input')
@click.option('--output', help='Path to output')
def run(input, output):
    config = open_yaml(input)
    run_requests(config, output)


if __name__ == '__main__':
    cli()