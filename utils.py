import os
import requests
import threading
from colorama import Fore, Style

HEADERS = {}
BASE_URL = ""
GUILD_ID = ""
CONFIG = {}
lock = threading.Lock()

delete_counter = 0
create_counter = 0
message_counter = 0
ban_counter = 0


def initialize_api(token, config):
    global HEADERS, CONFIG
    HEADERS = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    CONFIG = config
    return True


def set_guild_id(guild_id):
    global GUILD_ID, BASE_URL
    GUILD_ID = guild_id
    BASE_URL = f"https://discord.com/api/v10/guilds/{GUILD_ID}"


def get_headers():
    return HEADERS


def get_base_url():
    return BASE_URL


def get_guild_id():
    return GUILD_ID


def get_config():
    return CONFIG


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def gradient_text(text):
    colors = [Fore.LIGHTWHITE_EX, Fore.LIGHTRED_EX, Fore.RED]
    result = ""
    for i, char in enumerate(text):
        color_index = int(i * (len(colors) - 1) / (len(text) - 1)) if len(text) > 1 else 0
        result += colors[color_index] + char
    return result + Style.RESET_ALL


def fast_request(method, url, **kwargs):
    try:
        return requests.request(
            method, 
            url, 
            headers=HEADERS, 
            timeout=2,
            **kwargs
        )
    except Exception:
        return None


def increment_counter(counter_name):
    global delete_counter, create_counter, message_counter, ban_counter
    with lock:
        if counter_name == "delete":
            delete_counter += 1
            return delete_counter
        elif counter_name == "create":
            create_counter += 1
            return create_counter
        elif counter_name == "message":
            message_counter += 1
            return message_counter
        elif counter_name == "ban":
            ban_counter += 1
            return ban_counter
    return 0


def reset_counter(counter_name):
    global delete_counter, create_counter, message_counter, ban_counter
    if counter_name == "delete":
        delete_counter = 0
    elif counter_name == "create":
        create_counter = 0
    elif counter_name == "message":
        message_counter = 0
    elif counter_name == "ban":
        ban_counter = 0


def get_counter(counter_name):
    global delete_counter, create_counter, message_counter, ban_counter
    if counter_name == "delete":
        return delete_counter
    elif counter_name == "create":
        return create_counter
    elif counter_name == "message":
        return message_counter
    elif counter_name == "ban":
        return ban_counter
    return 0
