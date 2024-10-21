# OpenSanctions Look Up

This Python script allows users to perform searches using the OpenSanctions API. It supports querying by name, date of birth, company name, and address, among other parameters.

## Features

- Search by name and date of birth
- Search by company name
- Search by name and address
- Support for multiple queries in JSON format
- Outputs results to a text file named after the queried name

## Prerequisites

- Python 3.x
- Requests library
- Click library

You can install the required libraries using pip:

    pip install requests click

## Setting Up

Get your OpenSanctions API Key:

Sign up at OpenSanctions to obtain your API key.

Set the API Key as an Environment Variable: 

You need to export your API key in your terminal or command prompt. Use the following command:

    export OS_API_KEY="your_api_key_here"

## Running the Script

To run the script, navigate to the directory where the script is located and use the following command:


    python your_script_name.py

Replace your_script_name.py with the actual name of your Python script.
Usage

You can use the script to perform various queries. Here are some examples:

Query by Name and Date of Birth:

    python your_script_name.py query-name-dob

Query by Company Name:

    python your_script_name.py query-company

Query by Name and Address:

    python your_script_name.py query-name-address
    

## Output

The output of the search will be saved in a text file named after the queried name (e.g., barackobama.txt).

