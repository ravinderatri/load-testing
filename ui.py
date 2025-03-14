import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from threading import Thread
import shutil
import os
import zipfile
from request_handler import start_requests
from url_handler import validate_inputs

# Global flag to allow stopping execution
stop_flag = False

# Define directories and file paths
LOG_DIR = "logs"
RESULTS_DIR = "results"
ZIP_FILE = "result.zip"

def start_thread(api_urls_entry, total_requests_entry, concurrent_requests_entry, output_box, 
                 success_label, failure_label, time_label, start_button, loading_label, stop_button, download_button, zip_button):
    """Starts API requests in a separate thread"""
    global stop_flag
    stop_flag = False

    validated_data = validate_inputs(api_urls_entry, total_requests_entry, concurrent_requests_entry)
    if validated_data is None:
        return
    
    api_urls, total_requests, concurrent_requests = validated_data

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "Starting requests...\n")
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    loading_label.config(text="Processing...", fg="blue")

    def log_callback(message):
        """Updates the log output in the UI"""
        output_box.insert(tk.END, message)
        output_box.yview(tk.END)

    def run():
        """Runs API requests in a thread"""
        global stop_flag
        success, failure, exec_time, failure_reasons = start_requests(api_urls, total_requests, concurrent_requests, log_callback, lambda: stop_flag)

        time_label.config(text=f"Execution Time: {exec_time:.2f} sec")
        success_label.config(text=f"Success: {success}", fg="green")
        failure_label.config(text=f"Failed: {failure}", fg="red")

        if stop_flag:
            loading_label.config(text="Stopped!", fg="red")
            messagebox.showwarning("Stopped", "API Load Testing was manually stopped!")
        else:
            loading_label.config(text="Completed!", fg="green")
            messagebox.showinfo("Completed", "API Load Testing Completed!")

        # Show failure reasons
        if failure > 0:
            failure_details = "\n".join([f"{reason}: {count}" for reason, count in failure_reasons.items()])
            messagebox.showwarning("Failures Detected", f"Failed Requests: {failure}\n\nReasons:\n{failure_details}")

        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        download_button.config(state=tk.NORMAL)  # Enable download button after completion
        zip_button.config(state=tk.NORMAL)  # Enable ZIP download button after completion

    thread = Thread(target=run)
    thread.start()

def stop_requests():
    """Sets the stop flag to stop execution"""
    global stop_flag
    stop_flag = True

def download_files():
    """Allows the user to download the results CSV and logs"""
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        return  # If no folder is selected, exit the function
    
    try:
        # Copy logs and results files to the selected folder
        if os.path.exists(RESULTS_DIR):
            shutil.copytree(RESULTS_DIR, os.path.join(folder_selected, RESULTS_DIR), dirs_exist_ok=True)
        if os.path.exists(LOG_DIR):
            shutil.copytree(LOG_DIR, os.path.join(folder_selected, LOG_DIR), dirs_exist_ok=True)
        
        messagebox.showinfo("Download Complete", "Results and logs have been saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download files: {e}")

def download_zip():
    """Creates a ZIP file of logs and results and allows the user to download it"""
    try:
        with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add logs and results to the ZIP file
            for folder in [LOG_DIR, RESULTS_DIR]:
                if os.path.exists(folder):
                    for root, _, files in os.walk(folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, start='.'))

        # Ask user where to save the ZIP file
        zip_location = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")], initialfile="API_Test_Results.zip")
        if zip_location:
            shutil.move(ZIP_FILE, zip_location)
            messagebox.showinfo("Download Complete", f"ZIP file saved successfully at:\n{zip_location}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to create ZIP file: {e}")

# Tkinter UI setup
root = tk.Tk()
root.title("API Load Tester")
root.geometry("620x700")

# Labels and Entry Fields
tk.Label(root, text="API URLs (comma separated):").pack()
api_urls_entry = tk.Entry(root, width=60)
api_urls_entry.pack()

tk.Label(root, text="Total Requests per URL:").pack()
total_requests_entry = tk.Entry(root, width=10)
total_requests_entry.insert(0, "1000")
total_requests_entry.pack()

tk.Label(root, text="Concurrent Requests:").pack()
concurrent_requests_entry = tk.Entry(root, width=10)
concurrent_requests_entry.insert(0, "50")
concurrent_requests_entry.pack()

# Status Labels
loading_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
loading_label.pack()
time_label = tk.Label(root, text="Execution Time: 0 sec")
time_label.pack()
success_label = tk.Label(root, text="Success: 0")
success_label.pack()
failure_label = tk.Label(root, text="Failed: 0")
failure_label.pack()

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start Requests", command=lambda: start_thread(
    api_urls_entry, total_requests_entry, concurrent_requests_entry, output_box,
    success_label, failure_label, time_label, start_button, loading_label, stop_button, download_button, zip_button))
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Stop Requests", command=stop_requests, state=tk.DISABLED)
stop_button.grid(row=0, column=1, padx=5)

download_button = tk.Button(root, text="Download Logs & Results", command=download_files, state=tk.DISABLED)
download_button.pack(pady=5)

zip_button = tk.Button(root, text="Download ZIP", command=download_zip, state=tk.DISABLED)
zip_button.pack(pady=5)

# Output Box
output_box = scrolledtext.ScrolledText(root, height=15, width=75)
output_box.pack()

root.mainloop()
