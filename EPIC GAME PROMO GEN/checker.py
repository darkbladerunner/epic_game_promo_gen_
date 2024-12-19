import requests
import time
from urllib.parse import urlparse

def read_promos(file_path):
    """Read promo links from a file."""
    try:
        with open(file_path, "r") as file:
            promos = file.read().splitlines()
        return [promo.strip() for promo in promos if promo.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def is_valid_url(url):
    """Check if the URL is properly formatted."""
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

def check_promo(promo):
    """Check if a promo link is valid."""
    try:
        response = requests.get(promo, timeout=5)
        if response.status_code == 200:
            return "valid"
        elif response.status_code == 404:
            return "invalid"
        else:
            return "unknown"
    except requests.RequestException:
        return "error"

def main():
    file_path = "promo.txt"
    promos = read_promos(file_path)
    if not promos:
        print("No promos found. Ensure 'promo.txt' contains promo links.")
        return

    print(f"Checking {len(promos)} promos...")

    valid_count = 0
    invalid_count = 0
    duplicate_count = 0
    error_count = 0
    malformed_count = 0

    checked_promos = set()
    for promo in promos:
        if promo in checked_promos:
            duplicate_count += 1
            continue
        
        if not is_valid_url(promo):
            malformed_count += 1
            continue

        result = check_promo(promo)
        if result == "valid":
            valid_count += 1
        elif result == "invalid":
            invalid_count += 1
        else:
            error_count += 1

        checked_promos.add(promo)

    print("\n--- Promo Check Summary ---")
    print(f"Total Promos: {len(promos)}")
    print(f"Valid: {valid_count}")
    print(f"Invalid: {invalid_count}")
    print(f"Duplicates: {duplicate_count}")
    print(f"Malformed: {malformed_count}")
    print(f"Errors: {error_count}")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
