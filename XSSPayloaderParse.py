#This program will parse outputs from XSSPayloader's and alert you to any potential XSS vulerabilities
import re

def analyze_log_file(log_file):
    # Patterns to detect potential XSS vulnerabilities
    patterns = [
        r'<script[^>]*?>',  
        r'on[a-z]+=',       
        r'javascript:',     
        r'<img[^>]*?>',     
        r'<iframe[^>]*?>',  
        r'&lt;script&gt;', 
    ]
    
    # Load the logfile
    try:
        with open(log_file, 'r') as file:
            log_content = file.read()
    except FileNotFoundError:
        print(f"Error: The log file {log_file} does not exist.")
        return

    # Analyze the log content for potential XSS
    for pattern in patterns:
        matches = re.findall(pattern, log_content, re.IGNORECASE)
        if matches:
            print(f"Found {len(matches)} potential XSS indicators for pattern '{pattern}':")
            for match in matches[:10]:  # Show up to 10 matches per pattern
                print(f"  {match}")
            print("-" * 50)

    # Search for reflected payloads
    payloads_found = re.findall(r"Payload: (.+)", log_content)
    if payloads_found:
        print(f"\nPayloads reflected in the response:")
        for payload in payloads_found:
            if payload in log_content:
                print(f"  Reflected Payload: {payload}")
        print("-" * 50)

# Main execution
if __name__ == "__main__":
    log_file = input("Enter the path to the log file to analyze: ") or "/home/user/Desktop/Python/Test Results/xss_test_results.log"
    analyze_log_file(log_file)