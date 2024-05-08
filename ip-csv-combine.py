"""
Script Name: ip-csv-combine.py
Author: Justin Lund
Last modified: 04/15/24
Date created: 12/05/23
Version: 1.0

Purpose:
For use with splunk output from a DDoS (stats count by src_ip)
Used for checking if the same source IPs are seen across multiple traffic spikes
This will show how many CSVs the IP shows up in, as well as the total event count across all spreadsheets for each IP

Usage: python3 ip-csv-combine.py -i <input_directory> -o <output_file>

Notes:
- Requires pandas (pip3 install pandas)
- ***** This script is specifically looking for a field named src_ip *****
- Use the -i/--input switch to specify the directory containing CSV files
- Use the -o/--output switch to specify the output file name and location

Roadmap:
- Make column title selectable, rather than specifically targetting src_ip
   - Borrow code from domain-extract.py for this
"""

import pandas as pd
import glob
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Combine CSV files based on src_ip')
parser.add_argument('-i', '--input', type=str, required=True, help='Input directory containing CSV files')
parser.add_argument('-o', '--output', type=str, required=True, help='Output file path for the combined CSV')
args = parser.parse_args()

# Function to read and return data from a CSV
def read_csv(file_name):
    return pd.read_csv(file_name, usecols=['src_ip', 'count'])

# Directory containing your CSV files
csv_directory = args.input  # Directory specified by user

# Automatically find all CSV files in the specified directory
csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

# Check if any CSV files were found
if not csv_files:
    print("No CSV files found in the directory.")
else:
    # Read each CSV file
    dataframes = [read_csv(file) for file in csv_files]

    # Combine all data into a single DataFrame
    combined_df = pd.concat(dataframes)

    # Group by 'src_ip' and sum 'count', count 'Appearances'
    result_df = combined_df.groupby('src_ip').agg(
        total_count=pd.NamedAgg(column='count', aggfunc='sum'),
        Appearances=pd.NamedAgg(column='src_ip', aggfunc='size')
    ).reset_index()

    # Rename columns for clarity
    result_df.rename(columns={'src_ip': 'Source IP', 'total_count': 'Total Count'}, inplace=True)

    # Save to new CSV
    result_df.to_csv(args.output, index=False)

    print(f"Combined CSV created as '{args.output}'")
