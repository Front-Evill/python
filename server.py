import time
import base64
import requests
from colorama import Fore
from utils import fast_request, get_base_url, get_config, gradient_text


def change_server_icon():
    config = get_config()
    base_url = get_base_url()
    icon_url = config.get("server_icon_url", "")
    
    if not icon_url:
        print(Fore.RED + "Error: No server icon URL configured")
        time.sleep(3)
        return
    
    try:
        icon_response = requests.get(icon_url, timeout=10)
        
        if icon_response.status_code == 200:
            icon_base64 = base64.b64encode(icon_response.content).decode('utf-8')
            
            if '.png' in icon_url.lower():
                mime_type = "image/png"
            elif '.jpg' in icon_url.lower() or '.jpeg' in icon_url.lower():
                mime_type = "image/jpeg"
            elif '.gif' in icon_url.lower():
                mime_type = "image/gif"
            elif '.webp' in icon_url.lower():
                mime_type = "image/webp"
            else:
                mime_type = "image/jpeg"
            
            icon_data = f"data:{mime_type};base64,{icon_base64}"
            
            payload = {"icon": icon_data}
            response = fast_request("PATCH", base_url, json=payload)
            
            if response and response.status_code == 200:
                print(gradient_text("Done - Icon Changed Successfully"))
            else:
                print(Fore.RED + " Failed to Change Icon")
        else:
            print(Fore.RED + f" Failed to Download Icon (Status: {icon_response.status_code})")
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
    
    time.sleep(3)


def change_server_name():
    config = get_config()
    base_url = get_base_url()
    new_name = config.get("server_name", "Hacked Server")
    
    try:
        payload = {"name": new_name}
        response = fast_request("PATCH", base_url, json=payload)
        
        if response and response.status_code == 200:
            print(
                Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
                gradient_text(f" Server Name Changed to: {new_name}")
            )
        else:
            print(
                Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
                Fore.RED + " Failed to Change Server Name"
            )
    
    except Exception as e:
        print(
            Fore.RED + "[" + Fore.GREEN + "#" + Fore.RED + "]" +
            Fore.RED + f" Error: {str(e)}"
        )
    
    time.sleep(3)
