#This program requires command line arguments
import requests
import os
import time
import logging
import urllib.parse
import argparse

#Setup logging
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

# Define function to send payloads to url
def send_payloads(payloads, target_urls, param_name="q", delay=1, method="GET"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    for url in target_urls:
        for payload in payloads:
            encoded_payload = urllib.parse.quote(payload)
            
            if method.upper() == "POST":
                try:
                    response = requests.post(url, data={param_name: encoded_payload}, headers = headers)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    error_message = f"Request failed for payload: {payload} - {e}"
                    print(error_message)
                    logging.error(error_message)
                continue
            
            # Replaces place holder in url with payload
            url_with_payload = url.replace(f"{{{param_name}}}", encoded_payload)
        
            try:
                # Send request
                response = requests.get(url_with_payload, headers = headers)
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

    parser = argparse.ArgumentParser(description="Send payloads to target URLs for XSS testing.")
    parser.add_argument('payload_file', help="Path to the file containing payloads")
    parser.add_argument('target_urls', nargs='+', help="Target URLs with placeholders for injecting payloads")
    parser.add_argument('--param_name', default="q", help="Parameter name for payload injection")
    parser.add_argument('--delay', type=int, default=1, help="Delay between requests (in seconds)")
    parser.add_argument('--method', choices=['GET', 'POST'], default='GET', help="HTTP method to use")
    
    args = parser.parse_args()

    # Load the payloads from a file
    payloads = load_payloads(args.payload_file)
    
    # Send the payloads to the target URL
    send_payloads(payloads, args.target_urls, args.param_name, delay=args.delay, method=args.method)