"""
*** NOTE: This script is currently dependent on https://github.com/maldevel/IPGeoLocation ***

Script Name: ip-csv-lookup.py
Author: Justin Lund
Last modified: 04/15/24
Date created: 10/17/23
Version: 0.4

Purpose:
Obtain additional information on IP addresses
Use-case: Determining source ISP / Organization for DDoS activity

Parameters:
-h, --help [Show this help message and exit]
-i INPUT, --input INPUT [Input CSV file]
-o OUTPUT, --output OUTPUT [Output CSV file]

Usage: python3 ip-csv-lookup.py [-h] -i INPUT [-s] [-o OUTPUT] [-c]

Example:
python3 ip-csv-lookup.py -i splunk_data.csv -o output.csv

- Under # Configurable variables, set:
-- ipgeolocation.py script location
-- Number of IPs in the spreadsheet to look up
-- Column containing the IPs
- This will create a new CSV with new output fields; City, Country, Region Name, ISP, Organization, ASN

Roadmap:
- Make max entries (IP lookup limit) & CSV column configurable with parameters so the script doesn't need to be edited
- Have the script defaulted with the ipgeolocation.py location unspecified, and add an error message if the script source isn't added
- Incorporate the ipgeolocation.py script directly into this script
"""

import csv
import subprocess
import time
import argparse

### --------------------------------------------------------------- ###
### -------------------- CONFIGURABLE VARIABLES ------------------- ###
### --------------------------------------------------------------- ###

ipgeo_path = '/Users/jlund/scripts/IPGeoLocation/ipgeolocation.py'
max_entries = 300
target_column = 'src_ip'

### --------------------------------------------------------------- ###

# Argument parsing
parser = argparse.ArgumentParser(description='Process some IPs.')
parser.add_argument('-i', '--input', required=True, help='Input CSV file')
parser.add_argument('-o', '--output', required=True, help='Output CSV file')

args = parser.parse_args()
input_csv = args.input
output_csv = args.output

# Read the original CSV
rows = []
with open(input_csv, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rows.append(row)

# Process up to max_entries
for i, row in enumerate(rows[:max_entries]):
    ip = row[target_column]  # Use the variable here
    print(f"Processing {ip}...")
    result = subprocess.run(['python3', ipgeo_path, '-t', ip], capture_output=True, text=True)
    
    # Parsing City, Country, Region Name, ISP, Organization, and ASN from ipgeo output
    for line in result.stdout.split('\n'):
        if 'City: ' in line:
            row['City'] = line.split('City: ')[1]
        elif 'Country: ' in line:
            row['Country'] = line.split('Country: ')[1]
        elif 'Region Name: ' in line:
            row['Region Name'] = line.split('Region Name: ')[1]
        elif 'ISP: ' in line:
            row['ISP'] = line.split('ISP: ')[1]
        elif 'Organization: ' in line:
            row['Organization'] = line.split('Organization: ')[1]
        elif 'ASN: ' in line:
            row['ASN'] = line.split('ASN: ')[1]

    # Pause to avoid rate-limiting
    if i % 45 == 44:
        print("Sleeping for 60 seconds to avoid rate-limiting...")
        time.sleep(60)

# Write the updated CSV
with open(output_csv, 'w') as csv_file:
    # Correct the order to match your specifications
    default_fields = [field for field in rows[0].keys() if field not in ['City', 'Country', 'Region Name', 'ISP', 'Organization', 'ASN']]
    new_fields = ['City', 'Country', 'Region Name', 'ISP', 'Organization', 'ASN']
    fieldnames = default_fields + new_fields
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in rows:
        csv_writer.writerow(row)

print(f"Done. Updated CSV: {output_csv}.")
