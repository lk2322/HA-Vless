#!/usr/bin/env python3
"""
HAProxy Agent for Xray External Connectivity Checks

This script checks connectivity to external sites (Google, Cloudflare, etc.)
and reports the status to HAProxy via the agent-check protocol.
"""

import socket
import sys
import time
import ssl
import random
import logging
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException, Timeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/xray_agent_check.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('xray_agent_check')

# Sites to check for connectivity - can be overridden with XRAY_AGENT_TEST_SITES env var
DEFAULT_TEST_SITES = [
    "https://www.google.com",
    "https://www.cloudflare.com",
    "https://www.github.com",
    "https://www.apple.com",
    "https://www.microsoft.com",
]

# Get test sites from environment or use defaults
TEST_SITES = os.environ.get('XRAY_AGENT_TEST_SITES', ','.join(DEFAULT_TEST_SITES)).split(',')

# Number of successful checks required to consider the service up
SUCCESS_THRESHOLD = int(os.environ.get('XRAY_AGENT_SUCCESS_THRESHOLD', '3'))
# Maximum number of concurrent checks
MAX_WORKERS = int(os.environ.get('XRAY_AGENT_MAX_WORKERS', '5'))
# Timeout for connection attempts (seconds)
TIMEOUT = int(os.environ.get('XRAY_AGENT_TIMEOUT', '5'))
# Local agent socket port
AGENT_PORT = int(os.environ.get('XRAY_AGENT_PORT', '8192'))

def check_site(url, timeout=TIMEOUT):
    """Check a single site for connectivity using requests."""
    try:
        headers = {'User-Agent': 'XrayAgent/1.0'}
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code < 400:
            logger.debug(f"Successfully connected to {url}")
            return True
    except (RequestException, Timeout) as e:
        logger.warning(f"Failed to connect to {url}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error checking {url}: {e}")

    return False

def perform_connectivity_check():
    """
    Perform connectivity checks on multiple sites in parallel.
    Returns True if enough sites are reachable, False otherwise.
    """
    success_count = 0
    
    random.shuffle(TEST_SITES)
    sites_to_check = TEST_SITES[:SUCCESS_THRESHOLD + 1]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(check_site, url): url for url in sites_to_check}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    success_count += 1
                    if success_count >= SUCCESS_THRESHOLD:
                        return True
            except Exception as e:
                logger.error(f"Exception checking {url}: {e}")

    return success_count >= SUCCESS_THRESHOLD

def run_agent_server():
    """
    Run the HAProxy agent server that responds to health check requests.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(('0.0.0.0', AGENT_PORT))
        server_socket.listen(5)
        logger.info(f"Agent server listening on port {AGENT_PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            logger.debug(f"Connection from {addr}")

            try:
                result = perform_connectivity_check()
                if result:
                    response = "up\n"
                    logger.info("Reporting UP status to HAProxy")
                else:
                    response = "down\n"
                    logger.warning("Reporting DOWN status to HAProxy")

                client_socket.sendall(response.encode())
            except Exception as e:
                logger.error(f"Error during check: {e}")
                client_socket.sendall("down\n".encode())
            finally:
                client_socket.close()

    except KeyboardInterrupt:
        logger.info("Agent shutting down")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    logger.info("Starting Xray connectivity agent")
    run_agent_server()
