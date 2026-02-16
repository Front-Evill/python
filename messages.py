import time
import threading
from colorama import Fore
from utils import (
    fast_request, get_base_url, get_config, gradient_text,
    increment_counter, reset_counter, get_counter
)


def send_message_thread(channel_id, channel_name, message):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    payload = {"content": message}
    
    response = fast_request("POST", url, json=payload)
    
    if response and response.status_code in [200, 201]:
        count = increment_counter("message")
        print(
            Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
            gradient_text(f" Sent Message #{count} to Channel ID: {channel_id}")
        )
    time.sleep(0.2)


def fast_mass_message():
    reset_counter("message")
    base_url = get_base_url()
    config = get_config()
    
    spam_message = config.get("spam_message", "Hacked!")
    messages_per_channel = config.get("messages_per_channel", 5)
    
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
                    channel_type = channel.get('type', 0)
                    
                    if channel_type != 0:
                        continue
                    
                    for _ in range(messages_per_channel):
                        t = threading.Thread(
                            target=send_message_thread,
                            args=(channel_id, channel_name, spam_message)
                        )
                        threads.append(t)
                        t.start()
                        time.sleep(0.02)
            
            for t in threads:
                t.join()
            
            count = get_counter("message")
            print(Fore.LIGHTYELLOW_EX + f"\nSuccessfully Sent {count} Messages")
        else:
            print(Fore.RED + "Failed to Fetch Channels")
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    
    time.sleep(2)
