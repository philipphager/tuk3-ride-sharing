import click

from point_ride_sharing.service import RideSharing


@click.group()
def cli():
    pass


@cli.command()
@click.option('--output', required=True, help='Output path for trip to shared rides mapping')
@click.option('--distance', required=True, help='Max distance from start and endpoint in meter.', type=int)
@click.option('--time', required=True, help='Max time distance from start and endpoint in seconds.', type=int)
def shared_rides(output, distance, time):
    ride_sharing = RideSharing(output, distance, time)
    ride_sharing.run()


if __name__ == '__main__':
    cli()
