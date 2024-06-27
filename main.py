import requests
import time
import random
from colorama import init, Fore
import os
import schedule

init(autoreset=True)

def display_banner():
    banner = f"""
    {Fore.CYAN}=====================================================
    {Fore.CYAN}=          app.wildcard.lol | Auto Tipper           =
    {Fore.CYAN}=                 Github: IM-Hanzou                 =
    {Fore.CYAN}=====================================================
    {Fore.CYAN}= This is free script. Please dont sell this script =
    {Fore.CYAN}=              Use it at your own risk              =
    {Fore.CYAN}=====================================================
    """
    print(banner)

def get_bearer_tokens():
    """Reads bearer tokens from bearer.txt file"""
    try:
        with open('bearer.txt', 'r') as file:
            tokens = file.read().splitlines()
        return tokens
    except FileNotFoundError:
        print(f"{Fore.RED}bearer.txt not found. Please create the file with bearer tokens.")
        return []

def save_profile_data(profile_data):
    """Saves profile data to profil.txt, overwriting previous data"""
    with open('profil.txt', 'w') as file:
        for data in profile_data:
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")

def get_user_info(bearer_token):
    """Fetches user information using the bearer token"""
    url = "https://sys.wildcard.lol/app/my_profile"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            print(f"{Fore.RED}Token expired or invalid.")
            return None

        response.raise_for_status()
        
        data = response.json()
        farcaster_user = data["farcaster_user"]
        key_info = data["key"]
        points_holdings_all = data["points_holdings_all"][0]
        tipping_allowance_24h_all = data["tipping_allowance_24h_all"][0]
        earnings_24h_all = data["earnings_24h_all"][0]

        wallet_list = key_info.get("wallet", [])
        wallet_string = ", ".join(wallet_list) if wallet_list else "N/A"

        user_info = {
            "username": farcaster_user["username"],
            "fid": farcaster_user["fid"],
            "display_name": farcaster_user["display_name"],
            "custody_address": farcaster_user["custody_address"],
            "wallet_string": wallet_string,
            "points": f"{points_holdings_all['value']} {points_holdings_all['currency']}",
            "tipping_allowance": f"{tipping_allowance_24h_all['value']} {tipping_allowance_24h_all['currency']}",
            "earnings": f"{earnings_24h_all['value']} {earnings_24h_all['currency']}"
        }

        return user_info

    except requests.RequestException as e:
        print(f"{Fore.RED}Failed to get user information. Error: {str(e)}")
        return None

def display_topics(bearer_token):
    """Fetches and displays the list of topics available"""
    url = "https://sys.wildcard.lol/app/feed/topics"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        topics = response.json()

        print(f"\n{Fore.YELLOW}List Channel:")
        for i, topic in enumerate(topics, start=1):
            print(f"{Fore.GREEN}{i}. {topic['id']} | {topic['name']}")

        return topics

    except requests.RequestException as e:
        print(f"{Fore.RED}Failed to get channels. Error: {str(e)}")
        return None

def get_channel_info(bearer_token, channel_name, tip_amount):
    """Fetches trending casts from a specific channel and tips them"""
    url = f"https://sys.wildcard.lol/app/channel/{channel_name}/cast/trending"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        channel_data = response.json()

        print(f"\n{Fore.YELLOW}Trending Casts in Channel {channel_name}:")
        for cast in channel_data:
            farcaster_user = cast["farcaster_user"]
            cast_info = cast["cast"]
            cast_id = cast_info["id"]
            fid = farcaster_user["fid"]

            print(f"\n{Fore.MAGENTA}Username: {farcaster_user['username']}")
            print(f"{Fore.MAGENTA}Display Name: {farcaster_user['display_name']}")
            print(f"{Fore.MAGENTA}FID: {fid}")
            print(f"{Fore.CYAN}Cast ID: {cast_id}")
            print(f"{Fore.CYAN}Text: {cast_info['body']}")

            if tip_cast(bearer_token, cast_id, fid, tip_amount):
                print(f"{Fore.GREEN}Success Tip {tip_amount} WILD to Cast ID {cast_id}")
            else:
                print(f"{Fore.RED}Failed to tip Cast ID {cast_id}. Tip allowance may be limited.")
                break

            time.sleep(round(random.uniform(1, 5), 2))

    except requests.RequestException as e:
        print(f"{Fore.RED}Failed to get Casts. Error: {str(e)}")

def tip_cast(bearer_token, cast_id, fid, amount):
    """Sends a tip to a specific cast"""
    url = f"https://sys.wildcard.lol/app/tip/cast/{cast_id}/{fid}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Content-Type": "application/json"
    }
    data = {
        "currency": "WILD",
        "amount": amount,
        "fid": fid
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        return result.get("tip") == "success"

    except requests.RequestException as e:
        print(f"{Fore.RED}Failed to tip. Error: {str(e)}")
        return False

def get_casts_from_user(bearer_token, username):
    """Fetches the latest cast from a specific user"""
    url = f"https://sys.wildcard.lol/app/casts/{username}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        casts = response.json()
        if casts:
            top_cast = casts[0]
            farcaster_user = top_cast["farcaster_user"]
            cast_info = top_cast["cast"]
            cast_id = cast_info["id"]
            fid = farcaster_user["fid"]
            text = cast_info["body"]

            print(f"\n{Fore.YELLOW}Top Cast from {username}:")
            print(f"{Fore.MAGENTA}FID: {fid}")
            print(f"{Fore.CYAN}Cast ID: {cast_id}")
            print(f"{Fore.CYAN}Text: {text}")

            return cast_id, fid, text
        else:
            print(f"{Fore.RED}No casts found for user {username}.")
            return None, None, None

    except requests.RequestException as e:
        print(f"{Fore.RED}Failed to get casts for user {username}. Error: {str(e)}")
        return None, None, None

def tip_users(bearer_token, usernames, tip_amount):
    """Tips multiple users based on their latest cast"""
    for username in usernames:
        username = username.strip()
        cast_id, fid, _ = get_casts_from_user(bearer_token, username)
        if cast_id and fid:
            print(f"{Fore.YELLOW}Tipping user {username}...")
            if tip_cast(bearer_token, cast_id, fid, tip_amount):
                print(f"{Fore.GREEN}Successfully tipped {tip_amount} WILD to {username} for Cast ID {cast_id}.")
            else:
                print(f"{Fore.RED}Failed to tip {username} for Cast ID {cast_id}.")
        else:
            print(f"{Fore.RED}No valid cast found for {username}.")

def update_profile_data():
    """Updates profile data for all bearer tokens and saves to profil.txt"""
    bearer_tokens = get_bearer_tokens()
    if not bearer_tokens:
        return
    
    profile_data = []
    for token in bearer_tokens:
        user_info = get_user_info(token)
        if user_info:
            profile_data.append(user_info)
    
    save_profile_data(profile_data)
    return profile_data

def auto_tip_users(usernames, tip_amount):
    bearer_tokens = get_bearer_tokens()
    if not bearer_tokens:
        return

    for token in bearer_tokens:
        tip_users(token, usernames, tip_amount)

def auto_tip_channel(channel_name, tip_amount):
    bearer_tokens = get_bearer_tokens()
    if not bearer_tokens:
        return

    for token in bearer_tokens:
        get_channel_info(token, channel_name, tip_amount)

def schedule_auto_tip(option, usernames=None, channel_name=None, tip_amount=None):
    """Schedules the auto-tip function to run every 24 hours"""
    if option == 1:
        auto_tip_users(usernames, tip_amount)
        schedule.every(24).hours.do(auto_tip_users, usernames=usernames, tip_amount=tip_amount)
        print(f"{Fore.CYAN}Auto tipping to users scheduled every 24 hours.")
    elif option == 2:
        auto_tip_channel(channel_name, tip_amount)
        schedule.every(24).hours.do(auto_tip_channel, channel_name=channel_name, tip_amount=tip_amount)
        print(f"{Fore.CYAN}Auto tipping to channel scheduled every 24 hours.")

def main_menu():
    """Main menu for the script"""
    while True:
        print(f"{Fore.YELLOW}\nSelect options:")
        print(f"{Fore.CYAN}1. Tip to User(s)")
        print(f"{Fore.CYAN}2. Tip to User(s) From Channel List")
        print(f"{Fore.CYAN}3. View and Update Profiles")
        print(f"{Fore.CYAN}4. Auto Tip Every 24 Hours")
        print(f"{Fore.CYAN}5. Exit")

        try:
            option = int(input(f"{Fore.GREEN}Choose option (1, 2, 3, 4, or 5): "))
            if option not in [1, 2, 3, 4, 5]:
                print(f"{Fore.RED}Invalid option selected. Please try again.")
                continue

            if option == 5:
                print(f"{Fore.CYAN}Exiting. Goodbye!")
                break

            bearer_tokens = get_bearer_tokens()
            if not bearer_tokens:
                continue

            if option == 1:
                usernames = input(f"{Fore.GREEN}\nEnter the target username(s) (separated by comma | username1, username2, etc): ").strip().split(',')
                tip_amount = float(input(f"{Fore.GREEN}Enter tip amount in WILD: ").strip())
                for token in bearer_tokens:
                    tip_users(token, usernames, tip_amount)
            elif option == 2:
                topics = display_topics(bearer_tokens[0])  # Use the first token to get topics
                if topics:
                    topic_number = int(input(f"{Fore.GREEN}Enter the target channel number to tip: "))
                    if 1 <= topic_number <= len(topics):
                        channel_name = topics[topic_number - 1]["id"]
                        tip_amount = float(input(f"{Fore.GREEN}Enter tip amount in WILD: ").strip())
                        for token in bearer_tokens:
                            get_channel_info(token, channel_name, tip_amount)
                    else:
                        print(f"{Fore.RED}Invalid channel number. Returning to menu.")
                else:
                    print(f"{Fore.RED}No channels available. Returning to menu.")
            elif option == 3:
                profile_data = update_profile_data()
                if profile_data:
                    print(f"\n{Fore.YELLOW}Updated Profile Information:")
                    for data in profile_data:
                        for key, value in data.items():
                            print(f"{Fore.CYAN}{key.replace('_', ' ').capitalize()}: {Fore.MAGENTA}{value}")
                        print()
            elif option == 4:
                print(f"{Fore.GREEN}Choose auto tip mode:")
                print(f"{Fore.CYAN}1. Tip to User(s)")
                print(f"{Fore.CYAN}2. Tip to User(s) From Channel List")

                auto_tip_option = int(input(f"{Fore.GREEN}Choose option (1 or 2): "))
                if auto_tip_option not in [1, 2]:
                    print(f"{Fore.RED}Invalid option selected. Please try again.")
                    continue

                if auto_tip_option == 1:
                    usernames = input(f"{Fore.GREEN}\nEnter the target username(s) (separated by comma | username1, username2, etc): ").strip().split(',')
                    tip_amount = float(input(f"{Fore.GREEN}Enter tip amount in WILD: ").strip())
                    schedule_auto_tip(1, usernames=usernames, tip_amount=tip_amount)
                elif auto_tip_option == 2:
                    topics = display_topics(bearer_tokens[0])  # Use the first token to get topics
                    if topics:
                        topic_number = int(input(f"{Fore.GREEN}Enter the target channel number to tip: "))
                        if 1 <= topic_number <= len(topics):
                            channel_name = topics[topic_number - 1]["id"]
                            tip_amount = float(input(f"{Fore.GREEN}Enter tip amount in WILD: ").strip())
                            schedule_auto_tip(2, channel_name=channel_name, tip_amount=tip_amount)
                        else:
                            print(f"{Fore.RED}Invalid channel number. Returning to menu.")
                    else:
                        print(f"{Fore.RED}No channels available. Returning to menu.")

                while True:
                    schedule.run_pending()
                    time.sleep(1)

        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {str(e)}")

if __name__ == "__main__":
    display_banner()
    main_menu()
