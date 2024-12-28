#begin test_server.py
"""
Automated Functional Testing Script for server.py
"""

import os
import subprocess
import requests
import time
from pathlib import Path

# Constants
BASE_URL = "http://localhost:8000"
MESSAGES_DIR = "./messages"
TEST_MESSAGE = "Hello, this is a test message!"
PORT = 8000
SERVER_SCRIPT = "server.py"

# Utility functions
def start_server():
    """Start the server as a subprocess."""
    return subprocess.Popen(["python3", SERVER_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def stop_server(server_process):
    """Stop the server subprocess."""
    server_process.terminate()
    server_process.wait()

def check_url(url):
    """Check if a URL is accessible."""
    try:
        response = requests.get(url)
        return response.status_code == 200, response
    except requests.RequestException:
        return False, None

def submit_message(message):
    """Submit a message to the server."""
    try:
        response = requests.post(BASE_URL, data={"message": message})
        return response.status_code == 303
    except requests.RequestException:
        return False

def validate_message_file(index, content):
    """Check if a message file contains the expected content."""
    file_path = Path(MESSAGES_DIR) / f"message{index}.txt"
    if not file_path.exists():
        return False
    with open(file_path, "r") as file:
        return file.read().strip() == content

def check_chat_interface():
    """Validate the HTML interface reflects the messages correctly."""
    try:
        response = requests.get(BASE_URL)
        return TEST_MESSAGE in response.text
    except requests.RequestException:
        return False

# Test cases
def test_startup_and_shutdown():
    """Test server startup and shutdown."""
    server_process = start_server()
    time.sleep(2)  # Give the server time to start
    accessible, _ = check_url(BASE_URL)
    stop_server(server_process)
    assert accessible, "Server did not start successfully."
    print("[PASS] Server startup and shutdown")

def test_homepage_accessibility():
    """Test if the homepage is accessible."""
    server_process = start_server()
    time.sleep(2)
    accessible, response = check_url(BASE_URL)
    stop_server(server_process)
    assert accessible, "Homepage not accessible."
    assert "Chat Interface" in response.text, "Homepage content mismatch."
    print("[PASS] Homepage accessibility")

def test_message_submission():
    """Test submitting a message and verifying its persistence."""
    # Cleanup
    Path(MESSAGES_DIR).mkdir(exist_ok=True)
    for entry in Path(MESSAGES_DIR).iterdir():
        if entry.is_file():  # Ensure only files are deleted
            entry.unlink()

    server_process = start_server()
    time.sleep(2)
    submitted = submit_message(TEST_MESSAGE)
    time.sleep(2)
    stop_server(server_process)
    
    assert submitted, "Message submission failed."
    assert validate_message_file(1, TEST_MESSAGE), "Message not saved correctly."
    print("[PASS] Message submission")

def test_html_regeneration():
    """Test if the chat interface updates after a new message is submitted."""
    # Cleanup
    Path(MESSAGES_DIR).mkdir(exist_ok=True)
    for entry in Path(MESSAGES_DIR).iterdir():
        if entry.is_file():  # Ensure only files are deleted
            entry.unlink()

    server_process = start_server()
    time.sleep(2)
    submit_message(TEST_MESSAGE)
    time.sleep(2)
    updated = check_chat_interface()
    stop_server(server_process)
    
    assert updated, "Chat interface did not update."
    print("[PASS] HTML regeneration")

def test_file_handling():
    """Test handling of message files in the messages directory."""
    Path(MESSAGES_DIR).mkdir(exist_ok=True)
    for entry in Path(MESSAGES_DIR).iterdir():
        if entry.is_file():  # Ensure only files are deleted
            entry.unlink()

    # Create test files
    test_messages = ["Message 1", "Message 2", "Message 3"]
    for i, msg in enumerate(test_messages, start=1):
        with open(Path(MESSAGES_DIR) / f"message{i}.txt", "w") as file:
            file.write(msg)

    server_process = start_server()
    time.sleep(2)
    accessible, response = check_url(BASE_URL)
    stop_server(server_process)

    assert accessible, "Server not accessible after adding message files."
    for msg in test_messages:
        assert msg in response.text, f"Message '{msg}' not displayed on the interface."
    print("[PASS] File handling")

# Main execution
def run_tests():
    """Run all tests."""
    print("Starting tests...")
    test_startup_and_shutdown()
    test_homepage_accessibility()
    test_message_submission()
    test_html_regeneration()
    test_file_handling()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
#end test_server.py

