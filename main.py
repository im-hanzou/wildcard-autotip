import requests
import time
import random
from colorama import init, Fore

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

def get_user_info(bearer_token):
    url = "https://sys.wildcard.lol/app/my_profile"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }

    try:
        response = requests.get(url, headers=headers)
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

        print(f"\n{Fore.YELLOW}User Information:")
        for key, value in user_info.items():
            print(f"{Fore.CYAN}{key.replace('_', ' ').capitalize()}: {Fore.MAGENTA}{value}")

        return user_info

    except requests.RequestException as e:
        print(f"{Fore.RED}Failed to get user information. Token Expired: {str(e)}")
        return None

def display_topics(bearer_token):
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
        print(f"{Fore.RED}Failed to get channels. Token Expired: {str(e)}")
        return None

def get_channel_info(bearer_token, channel_name, tip_amount):
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
        print(f"{Fore.RED}Failed to get Casts. Token Expired: {str(e)}")

def tip_cast(bearer_token, cast_id, fid, amount):
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
        print(f"{Fore.RED}Failed to get casts for user {username}. Token Exprired: {str(e)}")
        return None, None, None

def tip_users(bearer_token, usernames, tip_amount):
    for username in usernames:
        username = username.strip()
        cast_id, fid, _ = get_casts_from_user(bearer_token, username)
        if cast_id and fid:
            print(f"{Fore.GREEN}Attempting to tip user {username}...")
            if tip_cast(bearer_token, cast_id, fid, tip_amount):
                print(f"{Fore.GREEN}Successfully tipped {tip_amount} WILD to {username} for Cast ID {cast_id}.")
            else:
                print(f"{Fore.RED}Failed to tip {username} for Cast ID {cast_id}.")
        else:
            print(f"{Fore.RED}No valid cast found for {username}.")

def main():
    display_banner()

    bearer_token = input(f"{Fore.GREEN}Enter Bearer Token: ").strip()

    user_info = get_user_info(bearer_token)
    if not user_info:
        print(f"{Fore.RED}Unable to proceed without valid user information.")
        return

    print(f"{Fore.YELLOW}\nSelect options:")
    print(f"{Fore.CYAN}1. Tip From Users")
    print(f"{Fore.CYAN}2. Tip From List Channels")

    try:
        option = int(input(f"{Fore.GREEN}Choose option (1 or 2): "))
        if option not in [1, 2]:
            print(f"{Fore.RED}Invalid option selected. Exiting.")
            return

        tip_amount = float(input(f"{Fore.GREEN}Enter tip amount in WILD: ").strip())

        if option == 1:
            usernames = input(f"{Fore.GREEN}Enter the username(s) (separated by comma | username1, username2, etc): ").strip().split(',')
            tip_users(bearer_token, usernames, tip_amount)
        elif option == 2:
            topics = display_topics(bearer_token)
            if topics:
                topic_number = int(input(f"{Fore.GREEN}Enter the channel number to tip: "))
                if 1 <= topic_number <= len(topics):
                    channel_name = topics[topic_number - 1]["id"]
                    get_channel_info(bearer_token, channel_name, tip_amount)
                else:
                    print(f"{Fore.RED}Invalid channel number. Exiting.")
            else:
                print(f"{Fore.RED}No channel available.")

    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
