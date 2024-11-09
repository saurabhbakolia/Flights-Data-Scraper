import click
import json
from flight_finder import FlightFinder
from datetime import datetime

@click.command()
@click.option("--from", "-f", "from_", required=True, help="The departure airport code.")
@click.option("--to", "-t", "to_", required=True, help="The arrival airport code.")
@click.option("--start", "-s", "start_", required=True, help="The departure date in YYYY-MM-DD format.")
@click.option("--end", "-e", "end_", help="The return date in YYYY-MM-DD format (optional).")
@click.option("--passengers", "-p", "passengers_", type=int, help="Number of passengers (default: 1).")
@click.option("--stops", "-c", "stops_", type=int, help="Maximum stops (default: non-stop).")
@click.option("--cheapest", "cheapest_", is_flag=True, help="Find the cheapest flight only.")
def search(from_, to_, start_, end_, passengers_, stops_, cheapest_):
    """
    Command-line interface to search for flights using specified options.
    """
    try:
        ff = FlightFinder(
            _from=from_,
            _to=to_,
            _start=start_,
            _end=end_,
            _passengers=passengers_,
            _stops=stops_
        )
        
        # Select the cheapest flight if the flag is set, else fetch all available flights
        if cheapest_:
            result = ff.find_flight()
        else:
            result = ff.find_flights()

        # Pretty-printing the JSON output
        result_data = json.loads(result)
        print(json.dumps(result_data, indent=2))

    except ValueError as ve:
        click.echo(f"Input Error: {ve}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

if __name__ == '__main__':
    search()
