import click

from service.sampler import Sampler


@click.group()
def cli():
    pass


@cli.command()
@click.option('--limit', default=100, help='Number of random trips selected from database')
def sample(limit):
    sampler = Sampler(limit)
    trips = sampler.get()
    print('Random trip sample (excluded all day trips), total:', limit)
    for trip in trips:
        print(trip)


if __name__ == '__main__':
    cli()
