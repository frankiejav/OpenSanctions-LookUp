import requests
import click
import os
from pprint import pprint

OS_API_KEY = os.getenv("OS_API_KEY")

BASE_URL = "https://api.opensanctions.org/match/default"

@click.group()
def cli():
    click.echo("\n" + "=" * 40)
    click.echo("        OpenSanctions Look Up")
    click.echo("=" * 40 + "\n")

@cli.command()
@click.option('--name', prompt="Enter the name", help="Search by name")
@click.option('--dob', default=None, prompt="Enter date of birth (YYYY-MM-DD)", help="Search by date of birth")
@click.option('--nationality', default=None, help="Filter by nationality (ISO country code)")
@click.option('--address', default=None, help="Search by address")
@click.option('--limit', default=5, help="Number of results to return")
def query_name_dob(name, dob, nationality, address, limit):
    """Search by name and date of birth."""
    query = {
        "queries": {
            "q1": {
                "schema": "Person",
                "properties": {
                    "name": [name],
                    "birthDate": [dob] if dob else [],
                    "nationality": [nationality] if nationality else [],
                    "address": [address] if address else []
                }
            }
        }
    }
    search(query, name)

@cli.command()
@click.option('--company', prompt="Enter company name", help="Search by company name")
@click.option('--jurisdiction', default=None, help="Filter by jurisdiction (ISO country code)")
@click.option('--regnum', default=None, help="Search by registration number")
@click.option('--limit', default=5, help="Number of results to return")
def query_company(company, jurisdiction, regnum, limit):
    """Search by company name, jurisdiction, and registration number."""
    query = {
        "queries": {
            "q1": {
                "schema": "Company",
                "properties": {
                    "name": [company],
                    "jurisdiction": [jurisdiction] if jurisdiction else [],
                    "registrationNumber": [regnum] if regnum else []
                }
            }
        }
    }
    search(query, company)

@cli.command()
@click.option('--name', prompt="Enter the name", help="Search by name")
@click.option('--address', default=None, help="Search by address")
@click.option('--country', default=None, help="Filter by country (ISO country code)")
def query_name_address(name, address, country):
    """Search by name and address."""
    query = {
        "queries": {
            "q1": {
                "schema": "Person",
                "properties": {
                    "name": [name],
                    "address": [address] if address else [],
                    "country": [country] if country else []
                }
            }
        }
    }
    search(query, name)

@cli.command()
@click.option('--queries', prompt="Enter queries in JSON format", help="Multiple queries in JSON format")
def multiple_queries(queries):
    """Perform multiple queries in one request."""
    try:
        query_dict = eval(queries)
        search(query_dict, "multiple_queries")
    except Exception as e:
        click.echo(f"Invalid query format: {e}")

def search(query, output):
    headers = {
        'Authorization': OS_API_KEY,
        'Content-Type': 'application/json'
    }
    results_output = []
    try:
        response = requests.post(BASE_URL, json=query, headers=headers)
        response.raise_for_status()
        
        for key, value in response.json().get("responses", {}).items():
            results = value.get("results", [])
            click.echo(f"\nResults for query '{key}':")
            if results:
                for idx, result in enumerate(results, start=1):
                    result_data = {
                        "id": result.get("id"),
                        "name": result.get("properties", {}).get("name"),
                        "match": result.get("match"),
                        "score": result.get("score"),
                        "features": result.get("features"),
                    }
                    results_output.append(result_data)
                    additional_info = result.get("properties", {})
                    result_data.update({
                        "additional_info": additional_info,
                        "match_score": result.get("score"),
                        "match_type": result.get("match")
                    })
                    pprint(result_data, sort_dicts=False)
            else:
                click.echo("No matches found.")
        
        filename = f"{output.replace(' ', '').lower()}.txt"
        with open(filename, 'w') as file:
            for item in results_output:
                file.write(f"{item}\n")
        click.echo(f"Results saved to {filename}")

    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        click.echo(f"Failed to query OpenSanctions API: {e}")

if __name__ == '__main__':
    cli()
