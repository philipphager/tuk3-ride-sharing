import click

from point_ride_sharing.service import RideSharing


@click.group()
def cli():
    pass


@cli.command()
@click.option('--output', required=True, help='Output path for trip to shared rides mapping')
@click.option('--distance', required=True, help='Max distance from start and endpoint in meter.', type=int)
@click.option('--time', required=True, help='Max time distance from start and endpoint in seconds.', type=int)
@click.option('--parallel', default=8, required=False, help='Number of threads', type=int)
def shared_rides(output, distance, time, parallel):
    distance = distance / 111120  # 1 Degree = 60 min, 1 min = 1852 m, 60 * 1852
    ride_sharing = RideSharing(output, distance, time, parallel)
    ride_sharing.run()


if __name__ == '__main__':
    cli()
