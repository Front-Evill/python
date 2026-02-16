import time
import threading
import random
from colorama import Fore
from utils import (
    fast_request, get_base_url, get_config, gradient_text,
    increment_counter, reset_counter, get_counter
)


def delete_channel_thread(channel_id, channel_name):
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    response = fast_request("DELETE", url)
    
    if response and response.status_code in [200, 204]:
        count = increment_counter("delete")
        print(gradient_text(f"Delete Channel ID: {channel_id}"))
    time.sleep(0.2)


def create_channel_thread(channel_name):
    base_url = get_base_url()
    url = f"{base_url}/channels"
    payload = {
        "name": channel_name,
        "type": 0
    }
    
    response = fast_request("POST", url, json=payload)
    
    if response and response.status_code in [200, 201]:
        count = increment_counter("create")
        print(gradient_text(f"Created Channel #{count} > {channel_name}"))
    time.sleep(0.2)


def rename_channel_thread(channel_id, old_name, new_name):
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    payload = {"name": new_name}
    
    response = fast_request("PATCH", url, json=payload)
    
    if response and response.status_code == 200:
        count = increment_counter("create")
        print(gradient_text(f"Renamed Channel #{count} > {old_name} to {new_name}"))
    time.sleep(0.2)


def delete_all_channels():
    reset_counter("delete")
    base_url = get_base_url()
    
    try:
        response = fast_request("GET", f"{base_url}/channels")
        
        if response and response.status_code == 200:
            channels = response.json()
            
            if not channels:
                print(Fore.RED + "No Channels Found")
                time.sleep(2)
                return
            
            threads = []
            for channel in channels:
                if isinstance(channel, dict) and 'id' in channel:
                    channel_id = channel['id']
                    channel_name = channel.get('name', 'Unknown')
                    t = threading.Thread(
                        target=delete_channel_thread,
                        args=(channel_id, channel_name)
                    )
                    threads.append(t)
                    t.start()
                    time.sleep(0.02)
            
            for t in threads:
                t.join()
            
            count = get_counter("delete")
            print(Fore.LIGHTYELLOW_EX + f"\nSuccessfully Deleted {count} Channels")
        else:
            print(Fore.RED + "Failed to Fetch Channels")
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    
    time.sleep(2)


def create_spam_channels():
    reset_counter("create")
    config = get_config()
    channel_names = config.get("channel_names", ["hacked"])
    num_channels = config.get("spam_channel_count", 50)
    
    try:
        threads = []
        for i in range(num_channels):
            channel_name = random.choice(channel_names)
            t = threading.Thread(
                target=create_channel_thread,
                args=(channel_name,)
            )
            threads.append(t)
            t.start()
            time.sleep(0.02)
        
        for t in threads:
            t.join()
        
        count = get_counter("create")
        print(Fore.LIGHTYELLOW_EX + f"\nSuccessfully Created {count} Channels")
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    
    time.sleep(2)


def rename_all_channels():
    reset_counter("create")
    base_url = get_base_url()
    config = get_config()
    channel_names = config.get("channel_names", ["renamed"])
    
    try:
        response = fast_request("GET", f"{base_url}/channels")
        
        if response and response.status_code == 200:
            channels = response.json()
            
            if not channels:
                print(Fore.RED + "No Channels Found")
                time.sleep(2)
                return
            
            threads = []
            for channel in channels:
                if isinstance(channel, dict) and 'id' in channel:
                    channel_id = channel['id']
                    old_name = channel.get('name', 'Unknown')
                    new_name = random.choice(channel_names)
                    t = threading.Thread(
                        target=rename_channel_thread,
                        args=(channel_id, old_name, new_name)
                    )
                    threads.append(t)
                    t.start()
                    time.sleep(0.02)
            
            for t in threads:
                t.join()
            
            count = get_counter("create")
            print(Fore.LIGHTYELLOW_EX + f"\nSuccessfully Renamed {count} Channels")
        else:
            print(Fore.RED + "Failed to Fetch Channels")
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    
    time.sleep(2)
