import requests
import json
import time

BASE_URL = "http://localhost:{PORT}"
LOGIN_ENDPOINT = "/{WEBPATH}/login"
ONLINE_ENDPOINT = "/{WEBPATH}/panel/inbound/onlines"
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
        if response.status_code == 200:
            return response.cookies
        return None
    except requests.exceptions.RequestException:
        return None

def fetch_inbound_onlines(cookies):
    online_url = f"{BASE_URL}{ONLINE_ENDPOINT}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/plain, */*",
    }
    try:
        response = requests.post(online_url, cookies=cookies, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def format_for_influxdb(data):
    timestamp = int(time.time() * 1000000000)
    user_count = len(data['obj']) if data and 'obj' in data else 0
    line = f"online_users,source=local_api user_count={user_count} {timestamp}"
    return line

def main():
    cookies = login_and_get_cookie()
    if not cookies:
        return
    data = fetch_inbound_onlines(cookies)
    if data:
        influxdb_line = format_for_influxdb(data)
        print(influxdb_line)

if __name__ == "__main__":
    main()
