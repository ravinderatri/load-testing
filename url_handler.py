# url_handler.py
import re
from tkinter import messagebox

def is_valid_url(url):
    """Validate a URL using a regular expression"""
    pattern = re.compile(
        r'^(https?://)?'  # http or https (optional)
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}|'  # Domain name
        r'localhost|'  # Localhost
        r'(\d{1,3}\.){3}\d{1,3})'  # IP Address
        r'(:\d+)?'  # Optional Port
        r'(/.*)?$'  # Path
    )
    return bool(pattern.match(url))

def validate_inputs(api_urls_entry, total_requests_entry, concurrent_requests_entry):
    """Validates API URLs and numeric inputs"""
    api_urls = [url.strip() for url in api_urls_entry.get().split(',') if url.strip()]
    total_requests = total_requests_entry.get().strip()
    concurrent_requests = concurrent_requests_entry.get().strip()

    if not api_urls:
        messagebox.showerror("Error", "Please enter at least one valid API URL")
        return None
    
    for url in api_urls:
        if not is_valid_url(url):
            messagebox.showerror("Error", f"Invalid URL: {url}")
            return None

    if not total_requests.isdigit() or int(total_requests) <= 0:
        messagebox.showerror("Error", "Total Requests must be a positive integer")
        return None

    if not concurrent_requests.isdigit() or int(concurrent_requests) <= 0:
        messagebox.showerror("Error", "Concurrent Requests must be a positive integer")
        return None

    return api_urls, int(total_requests), int(concurrent_requests)
