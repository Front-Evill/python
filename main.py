
import json
import sys
import time
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Import custom modules
try:
    from utils import clear_screen, gradient_text, initialize_api
    from ui import display_menu, get_server_selection
    from channels import delete_all_channels, create_spam_channels, rename_all_channels
    from roles import delete_all_roles, create_spam_roles
    from messages import fast_mass_message
    from members import ban_all_members
    from server import change_server_icon, change_server_name
except ImportError as e:
    sys.exit(1)


def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(Fore.RED + "Error: config.json not found!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(Fore.RED + f"Error parsing config.json: {e}")
        sys.exit(1)


def main():
    try:
        # Load configuration
        config = load_config()
        
        # Get bot token
        token = input(
            Fore.LIGHTRED_EX + "[" + Fore.GREEN + "#" + Fore.RED + "]" + 
            Fore.GREEN + " Enter Your Bot Token: " + Fore.RED + ": " + Fore.GREEN
        ).strip()
        
        if not token:
            print(Fore.RED + "Error: Token cannot be empty!")
            sys.exit(1)
        
        api_initialized = initialize_api(token, config)
        
        if not api_initialized:
            print(Fore.RED + "Failed to initialize API. Exiting...")
            sys.exit(1)
        
        guild_info = get_server_selection()
        
        if not guild_info:
            print(Fore.RED + "Failed to select server. Exiting...")
            sys.exit(1)
        
        # Main menu
        while True:
            clear_screen()
            choice = display_menu(guild_info, config)
            
            if choice is None:
                break
            
            # Execute selected action
            if choice in ["1", "#1", "01", "١"]:
                delete_all_channels()
            elif choice in ["2", "#2", "02", "٢"]:
                create_spam_channels()
            elif choice in ["3", "#3", "03", "٣"]:
                rename_all_channels()
            elif choice in ["4", "#4", "04", "٤"]:
                delete_all_roles()
            elif choice in ["5", "#5", "05", "٥"]:
                fast_mass_message()
            elif choice in ["6", "#6", "06", "٦"]:
                ban_all_members()
            elif choice in ["7", "#7", "07", "٧"]:
                change_server_icon()
            elif choice in ["8", "#8", "08", "٨"]:
                change_server_name()
            elif choice in ["9", "#9", "09", "٩"]:
                create_spam_roles()
            elif choice in ["0", "#0", "xx", "00", "XX", "Xx", "xX", "٠"]:
                print(gradient_text("        Good Bye..."))
                time.sleep(1)
                break
            else:
                print(Fore.RED + "\nInvalid Choice")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(Fore.LIGHTYELLOW_EX + "\n\nProgram Interrupted by User\n")
    except Exception as e:
        print(Fore.RED + f"\nFatal Error: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
