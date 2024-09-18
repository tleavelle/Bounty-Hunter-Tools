
import requests
import logging
import urllib.parse 
import base64 
from datetime import datetime

# Setup logging for verbose output
def setup_logging():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = f"sql_injection_log_{timestamp}.log"
    logging.basicConfig(filename=log_filename, 
                        level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return log_filename

# Interactive SQL payload input
def get_sql_payloads_interactive():
    payloads = []
    while True:
        payload = input("Enter a SQL payload (or type 'done' to finish): ")
        if payload.lower() == 'done':
            break
        payloads.append(payload)
    return payloads

# File-based SQL payload input
def get_sql_payloads_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            payloads = [line.strip() for line in file if line.strip()]
        return payloads
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []

# Encode SQL payloads (URL or Base64)
def encode_payload(payload, encoding_type):
    if encoding_type == 'url':
        return urllib.parse.quote(payload)
    elif encoding_type == 'base64':
        return base64.b64encode(payload.encode()).decode()
    return payload

# Method selection for payload input
def choose_sql_payload_input_method():
    choice = input("Would you like to input payloads manually or use a file? (manual/file): ").strip().lower()
    if choice == 'manual':
        return get_sql_payloads_interactive()
    elif choice == 'file':
        filepath = input("Enter the path to the SQL payloads file: ")
        return get_sql_payloads_from_file(filepath)
    else:
        print("Invalid choice, defaulting to manual input.")
        return get_sql_payloads_interactive()

# Function to test SQL injection on a target
def test_sql_injection(url, payloads, user_agent, encoding_type):
    headers = {'User-Agent': user_agent}
    for payload in payloads:
        try:
            encoded_payload = encode_payload(payload, encoding_type)
            # Assuming the vulnerable parameter is 'id' (can be adjusted)
            test_url = f"{url}?id={encoded_payload}"
            response = requests.get(test_url, headers=headers)
            log_result(payload, encoded_payload, response)
        except requests.RequestException as e:
            logging.error(f"Error with payload '{payload}': {e}")

# Log the result of each payload attempt
def log_result(original_payload, encoded_payload, response):
    logging.info(f"Original Payload: {original_payload}")
    logging.info(f"Encoded Payload: {encoded_payload}")
    logging.info(f"Response Status Code: {response.status_code}")
    if "error" in response.text.lower() or "syntax" in response.text.lower():
        logging.warning(f"Potential SQL error found in response for payload '{encoded_payload}'")
    else:
        logging.info(f"No SQL error found for payload '{encoded_payload}'")

# Main program
def main():
    log_file = setup_logging()
    print("Welcome to the SQL Injection Tester.")
    url = input("Enter the target URL (e.g., http://example.com/vulnerable.php): ")
    user_agent = input("Enter a custom User-Agent (or press enter for default): ").strip()
    if not user_agent:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    
    encoding_type = input("Choose encoding for payloads (none/url/base64): ").strip().lower()
    sql_payloads = choose_sql_payload_input_method()

    if sql_payloads:
        print(f"Testing {len(sql_payloads)} payload(s) on {url}")
        test_sql_injection(url, sql_payloads, user_agent, encoding_type)
        print(f"Testing complete. Results logged to {log_file}.")
    else:
        print("No payloads to test.")

def main_loop():
    while True:
        main()
        again = input("Do you want to test another URL or run more payloads? (yes/no): ").strip().lower()
        if again != 'yes':
            print("Exiting the program.")
            break

        
if __name__ == "__main__":
    main_loop()
