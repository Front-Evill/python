import time
import threading
from colorama import Fore
from utils import (
    fast_request, get_base_url, get_config, gradient_text,
    increment_counter, reset_counter, get_counter
)


def ban_member_thread(user_id, username):
    base_url = get_base_url()
    url = f"{base_url}/bans/{user_id}"
    
    config = get_config()
    delete_days = config.get("ban_delete_message_days", 7)
    
    payload = {"delete_message_days": delete_days}
    
    response = fast_request("PUT", url, json=payload)
    
    if response and response.status_code == 204:
        count = increment_counter("ban")
        print(
            Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
            gradient_text(f" Banned Member #{count} (ID: {user_id})")
        )
    time.sleep(0.02)


def ban_all_members():
    reset_counter("ban")
    base_url = get_base_url()
    
    try:
        url = f"{base_url}/members?limit=1000"
        response = fast_request("GET", url)
        
        if response and response.status_code == 200:
            members = response.json()
            
            if not members:
                print(
                    Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
                    Fore.WHITE + " No Members Found"
                )
                time.sleep(2)
                return
            
            threads = []
            for member in members:
                if (isinstance(member, dict) and 
                    'user' in member and 
                    isinstance(member['user'], dict) and 
                    'id' in member['user']):
                    
                    user_id = member['user']['id']
                    username = member['user'].get('username', 'Unknown')
                    
                    t = threading.Thread(
                        target=ban_member_thread,
                        args=(user_id, username)
                    )
                    threads.append(t)
                    t.start()
                    time.sleep(0.02)
            
            for t in threads:
                t.join()
            
            count = get_counter("ban")
            print(
                Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
                Fore.LIGHTYELLOW_EX + f"\nSuccessfully Banned {count} Members"
            )
        else:
            print(
                Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
                Fore.RED + " Failed to Fetch Members"
            )
    
    except Exception as e:
        print(
            Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
            Fore.RED + f" Error: {str(e)}"
        )
    
    time.sleep(2)
