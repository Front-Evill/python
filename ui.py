import time
import requests
from colorama import Fore
from utils import (
    clear_screen, gradient_text, get_headers,
    set_guild_id, get_config
)


def get_server_selection():
    clear_screen()
    headers = get_headers()
    
    print(Fore.WHITE + "\n" + Fore.RED + "Fetching Servers" + Fore.WHITE + "\n")
    
    try:
        url = "https://discord.com/api/v10/users/@me/guilds"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            guilds = response.json()
            
            if not guilds:
                print(Fore.RED + "No Servers Found")
                time.sleep(2)
                return None
            
            for idx, guild in enumerate(guilds, 1):
                print(
                    Fore.RED + f"[{idx}] " + 
                    Fore.WHITE + f"{guild['name']} " + 
                    Fore.RED + f"| ID: {guild['id']}"
                )
            
            choice = input(gradient_text("\nSelect Server Number: "))
            
            try:
                selected = guilds[int(choice) - 1]
                guild_id = selected['id']
                
                set_guild_id(guild_id)
                
                base_url = f"https://discord.com/api/v10/guilds/{guild_id}"
                guild_response = requests.get(base_url, headers=headers, timeout=5)
                
                guild_info = {
                    'id': guild_id,
                    'name': selected['name'],
                    'owner': 'Unknown',
                    'members': 'Unknown',
                    'bot_name': 'Unknown'
                }
                
                if guild_response.status_code == 200:
                    guild_data = guild_response.json()
                    
                    owner_id = guild_data.get('owner_id', 'Unknown')
                    owner_url = f"https://discord.com/api/v10/users/{owner_id}"
                    owner_response = requests.get(owner_url, headers=headers, timeout=5)
                    
                    if owner_response.status_code == 200:
                        owner_data = owner_response.json()
                        guild_info['owner'] = owner_data.get('username', 'Unknown')
                    
                    guild_info['members'] = guild_data.get('approximate_member_count', 'Unknown')
                    guild_info['name'] = guild_data.get('name', guild_info['name'])
                
                bot_url = "https://discord.com/api/v10/users/@me"
                bot_response = requests.get(bot_url, headers=headers, timeout=5)
                
                if bot_response.status_code == 200:
                    bot_data = bot_response.json()
                    guild_info['bot_name'] = bot_data.get('username', 'Unknown')
                
                return guild_info
            
            except (ValueError, IndexError):
                print(Fore.RED + "\nInvalid Selection")
                time.sleep(2)
                return None
        else:
            print(Fore.RED + "Failed to Fetch Servers")
            time.sleep(2)
            return None
    
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
        time.sleep(2)
        return None


def display_menu(guild_info, config):
    """Display the main menu and get user choice"""
    print()
    print()
    print()
    
    banner = f"""
        
{Fore.LIGHTRED_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠤⠤⠤⣄⡠⠤⠐⠐⠐⠐⠐⠐⠐⠐⣲⣤⣤⣄⡀    
{Fore.LIGHTRED_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⣒⣽⡶⠞⠛⠛⠛⠛⢶⣝⢶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄
{Fore.LIGHTRED_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠞⢡⣾⠏⠁⠀⠀⠀⠀⠀⣀⣀⣽⣆⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
{Fore.LIGHTRED_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣖⠉⠉⠀⠀⠀⠉⠓⠒⠒⠒⠒⠲⠾⠧⠤⢤⣿⣧⠙⠻⠿⠿⠿⣟⣛⣛⡛⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠙⠒⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.LIGHTRED_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠲⡦⢬⣭⣉⣑⣒⣶⣤⣤⡤⢶⠶⣤⡄⣀⣀⣀⡹⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.LIGHTRED_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⢀⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣤⡀⠀⠳⢾⣿⣿⠿⠿⠟⢁⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠉⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.LIGHTRED_EX}⠀⠀⠀⠀⠀⠀   ⣿⣀⢠⣿⢟⠻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠠⠈⠉⠙⢻⣿⣿⣿⣋⣀⣀⣠⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.LIGHTRED_EX} ⠀⠀⠀⠀⠀⠀⠀⠀⢹⡈⢹⣿⠴⣶⢾⡇⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⢸⣿⣿⣿⣿⣧⠀⢷⣶⣶⣶⣶⠋⣲⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⡶⠀⠀⠀
{Fore.LIGHTRED_EX} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠾⣿⡶⠙⣿⣿⣀⣀⣀⣉⣉⣉⣉⣉⣉⣉⣉⣉⣸⣿⣿⣿⣿⣿⣄⣈⣉⣉⣭⣥⣶⡾⠿⠿⠿⠿⠟⠛⣿⣿⣿⣿⣋⣁
{Fore.LIGHTRED_EX}     ⠀    ⠤⣬⣽⠖⣿⣿⣿⣿⣷⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣷⣾⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿


{Fore.LIGHTWHITE_EX}                                                                                      Name Your Bot    : {Fore.GREEN}{guild_info.get('bot_name', 'Unknown')}
{Fore.LIGHTWHITE_EX}                                                                                      ID SERVER        : {Fore.GREEN}{guild_info.get('id', 'Unknown')}
{Fore.LIGHTWHITE_EX}                                                                                      OWNER SERVER     : {Fore.GREEN}{guild_info.get('owner', 'Unknown')}
{Fore.LIGHTWHITE_EX}                                                                                      Member Server    : {Fore.GREEN}{guild_info.get('members', 'Unknown')}


{Fore.WHITE}                       {Fore.RED}Are{Fore.LIGHTWHITE_EX} you ready {Fore.RED} for {Fore.LIGHTWHITE_EX} more {Fore.RED}Problems{Fore.LIGHTWHITE_EX}??
{Fore.WHITE}                                            {Fore.RED}By {Fore.WHITE}-= {Fore.LIGHTGREEN_EX}FrontEvill{Fore.WHITE} -=
{Fore.RED}     ═══════════════════════════════════════════════════════════════
    """
    
    print(banner)
    
    menu_options = [
        ("1", "Delete Channels"),
        ("2", "Create Channels"),
        ("3", "Rename Channels"),
        ("4", "Delete Roles"),
        ("5", "Fast Mass Message"),
        ("6", "Ban All Members"),
        ("7", "Change Server Icon"),
        ("8", "Change Server Name"),
        ("9", "Create Roles"),
        ("xx", "Exit")
    ]
    
    for num, option in menu_options:
        print(
            Fore.LIGHTYELLOW_EX + "               " + 
            Fore.RED + "⟨" + Fore.GREEN + f"#{num}" + Fore.RED + "⟩" + 
            Fore.LIGHTRED_EX + "  >  " + 
            gradient_text(f" {option}      ")
        )
    
    print()
    print()
    
    try:
        choice = input(
            Fore.RED + "  ┌(" + Fore.GREEN + "Lithyom Gosh" + Fore.RED + ")-" +
            "[" + Fore.GREEN + "root" + Fore.RED + "]\n" +
            Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.RED
        ).strip()
        
        return choice
    
    except KeyboardInterrupt:
        print(Fore.LIGHTYELLOW_EX + "\n\nProgram Interrupted by User\n")
        return None
    except Exception as e:
        print(Fore.RED + f"\nError: {str(e)}\n")
        time.sleep(0.3)
        return None
