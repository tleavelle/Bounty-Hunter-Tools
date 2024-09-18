#This program requres you to hand type the URL's and prompts you for neccessary arguments
import requests
import os
import time
import logging
import urllib.parse

# Setup logging
logging.basicConfig(filename='xss_test_results.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define function that loads payloads and handles basic errors
def load_payloads(filename):
    if not os.path.isfile(filename):
        print(f"Error: File {filename} does not exist.")
        return []
    with open(filename, 'r') as file:
        payloads = [line.strip() for line in file if not line.startswith("#")]
    return payloads

# Define function to format the output
def format_output(payload, status_code, body):
    return f"Payload: {payload}\nStatus Code: {status_code}\nResponse Body:\n{body}\n"

# Define function to send payloads to URL
def send_payloads(payloads, target_urls, param_name="q", delay=1, method="GET"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    for url in target_urls:
        for payload in payloads:
            encoded_payload = urllib.parse.quote(payload)
            
            if method.upper() == "POST":
                try:
                    response = requests.post(url, data={param_name: encoded_payload}, headers=headers)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    error_message = f"Request failed for payload: {payload} - {e}"
                    print(error_message)
                    logging.error(error_message)
                continue
            
            # Replace placeholder in URL with payload
            url_with_payload = url.replace(f"{{{param_name}}}", encoded_payload)
        
            try:
                # Send request
                response = requests.get(url_with_payload, headers=headers)
                response.raise_for_status()

                # Log and print the formatted output
                output = format_output(payload, response.status_code, response.text)
                logging.info(output)
                print(output)

                # Delay for requests
                time.sleep(delay)  # Sleeps for the specified delay

            except requests.exceptions.RequestException as e:
                error_message = f"Request failed for payload: {payload} - {e}"
                print(error_message)
                logging.error(error_message)

# Main execution
if __name__ == "__main__":
    # Prompt the user for input
    payload_file = input("Enter the path to the payload file: ") or "/home/user/Desktop/Stuff/xssPayloads.txt"
    target_urls_input = input("Enter target URLs with placeholders for injecting payloads (separated by spaces): ")
    target_urls = target_urls_input.split()
    param_name = input("Enter the parameter name for payload injection (default 'q'): ") or "q"
    delay = input("Enter delay between requests in seconds (default 1): ")
    delay = int(delay) if delay else 1
    method = input("Enter HTTP method to use (GET or POST, default 'GET'): ").upper() or "GET"
    
    if method not in ['GET', 'POST']:
        print("Invalid HTTP method. Defaulting to GET.")
        method = "GET"
    
    # Load the payloads from a file
    payloads = load_payloads(payload_file)
    
    # Send the payloads to the target URL
    send_payloads(payloads, target_urls, param_name=param_name, delay=delay, method=method)