import os
import requests
import concurrent.futures
import time
import csv
import threading

# Ensure directories exist on Mac, Linux, and Windows
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

CSV_FILE = os.path.join(RESULTS_DIR, "request_results.csv")
LOG_FILE = os.path.join(LOGS_DIR, "request_logs.txt")

def send_request(session, request_id, api_url, success_count, failure_count, results, failure_reasons, log_callback, lock):
    """Sends a request and stores results in CSV with failure reasons."""
    failure_reason = ""   

    try:
        response = session.get(api_url, timeout=5)
        status_code = response.status_code

        if 200 <= status_code < 300:
            with lock:
                success_count[0] += 1
                results.append([request_id, api_url, status_code, "Success", ""])
        else:
            failure_reason = f"HTTP {status_code}"

    except requests.exceptions.Timeout:
        failure_reason = "Timeout Error"
    except requests.exceptions.ConnectionError:
        failure_reason = "Connection Error"
    except requests.exceptions.RequestException as e:
        failure_reason = str(e)

    # Handle failures outside the try-except block
    if failure_reason:
        with lock:
            failure_count[0] += 1
            failure_reasons[failure_reason] = failure_reasons.get(failure_reason, 0) + 1
            results.append([request_id, api_url, "N/A", "Failed", failure_reason])

        log_message = f"Request {request_id} to {api_url} failed: {failure_reason}\n"
        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_message)
        log_callback(log_message)
    else:
        log_callback(f"Request {request_id} to {api_url}: {status_code}\n")


def start_requests(api_urls, total_requests, concurrent_requests, log_callback, stop_callback):
    """Runs API load test with failure logging and manual stopping."""
    success_count = [0]
    failure_count = [0]
    failure_reasons = {}
    results = []
    lock = threading.Lock()

    start_time = time.time()

    # Ensure CSV and log directories exist
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Create CSV with headers before starting requests
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Request ID", "API URL", "Status Code", "Result", "Failure Reason"])

    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = []
            for api_url in api_urls:
                for i in range(total_requests):
                    if stop_callback():
                        log_callback("Stopping requests...\n")
                        break
                    futures.append(executor.submit(send_request, session, i, api_url, success_count, failure_count, results, failure_reasons, log_callback, lock))

            # Process completed requests
            for future in concurrent.futures.as_completed(futures):
                future.result()  # Ensures exceptions are raised if any

    end_time = time.time()
    exec_time = end_time - start_time

    # Write results to CSV
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

    return success_count[0], failure_count[0], exec_time, failure_reasons
