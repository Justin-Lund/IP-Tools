# domain-extract.py

Extract 2nd-level & top-level domains from URLs in a CSV, accounting for multi-tiered domains such as `.co.uk`

ie: `123.abc.domain.co.uk/definitely/not/phishing.html` will retutrn `domain.co.uk`

&nbsp;

# extract-ips.sh

Find & extract all IP addresses found in a target text file.

&nbsp;

# ip-csv-combine.py

Count how many times an IP address appears across multiple CSV files.

Intended for use with Splunk `stats count by src_ip` exports, and was specifically made for reviewing IP frequency across multiple DDoS attacks.

&nbsp;

# ip-csv-lookup.py

Run a lookup against multiple IP addresses from an input CSV, returning the following fields:

- City / Country / Region
- ISP / Organization / ASN

Note that the current version of the script requires this script as well: https://github.com/maldevel/IPGeoLocation

This will eventually be updated to be a standalone script.

There are 3 configurable variables at the top of the script:

- `ipgeo_path`: Set the path to your copy of the aforementioned IPGeoLocation script.
- `max_entries`: Limit of IP addresses to look up.
- `target_column`: The column header of the CSV that the script is looking for. Defaults to `src_ip`
