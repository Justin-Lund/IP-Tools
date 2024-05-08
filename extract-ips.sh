#!/bin/bash

# Script Name: extract-ips.sh
# Author: Justin Lund
# Date Created: 04/15/23
# Last Modified: 06/06/23
# Version: 1.0
#
# Purpose:
#   Extract any IP addresses found in target text file
#
# Usage:
#   ./extract-ips.sh -i input_file.txt [-o output_file.txt]

######################################

# Default file names
input_file=""
output_file=""

# Process command line options
while getopts "i:o:" opt; do
  case "$opt" in
    i) input_file="$OPTARG" ;;
    o) output_file="$OPTARG" ;;
    ?) echo "Usage: $0 -i input_file [-o output_file]"; exit 1 ;;
  esac
done

# Check if input file name is provided
if [ -z "$input_file" ]; then
  echo "Error: Input file name is required."
  echo "Usage: $0 -i input_file [-o output_file]"
  exit 1
fi

# Extract IP addresses using grep
ip_addresses=$(grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" "$input_file")

# Sort and deduplicate IP addresses
sorted_ips=$(echo "$ip_addresses" | sort -u)

# Check if an output file is specified
if [ -z "$output_file" ]; then
  # No output file specified, print to screen
  echo "IP addresses found:"
  echo "$sorted_ips"
else
  # Write sorted and deduplicated IP addresses to output file
  echo "$sorted_ips" > "$output_file"
  echo "IP addresses extracted and saved to $output_file."
fi
