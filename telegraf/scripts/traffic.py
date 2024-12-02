import requests
import json
import time

BASE_URL = "http://localhost:{PORT}"
LOGIN_ENDPOINT = "/{WEBPATH}/login"
INBOUNDS_LIST_ENDPOINT = "/{WEBPATH}/panel/api/inbounds/list"
USERNAME = "{USERNAME}"
PASSWORD = "{PASSWORD}"

def login_and_get_cookie():
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }
    try:
        response = requests.post(login_url, data=login_data, headers=headers)
        response.raise_for_status()
        return response.cookies
    except requests.exceptions.RequestException:
        return None

def fetch_clients_list(cookies):
    inbounds_url = f"{BASE_URL}{INBOUNDS_LIST_ENDPOINT}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/plain, */*",
    }
    try:
        response = requests.get(inbounds_url, cookies=cookies, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def format_for_influxdb(clients_data):
    timestamp = int(time.time() * 1000000000)  # nanoseconds
    lines = []
    if isinstance(clients_data, list):
        for client in clients_data:
            # Escape special characters in email for InfluxDB line protocol
            escaped_email = client.get("email", "unknown").replace(" ", "\\ ")
            lines.append(
                f"clients,source=local_api,email={escaped_email} up={client.get('up', 0)},down={client.get('down', 0)},enable={int(client.get('enable', False))} {timestamp}"
            )
    return lines

def main():
    cookies = login_and_get_cookie()
    if not cookies:
        return
    
    clients_data = fetch_clients_list(cookies)
    if clients_data and 'obj' in clients_data:
        clients = []
        for inbound in clients_data['obj']:
            if 'clientStats' in inbound and isinstance(inbound['clientStats'], list):
                for client in inbound['clientStats']:
                    client_data = {
                        "email": client.get("email", "unknown"),
                        "up": client.get("up", 0),
                        "down": client.get("down", 0),
                        "enable": client.get("enable", False)
                    }
                    clients.append(client_data)
        
        if clients:
            influxdb_lines = format_for_influxdb(clients)
            for line in influxdb_lines:
                print(line)

if __name__ == "__main__":
    main()
