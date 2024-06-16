import requests
import time
import random
from colorama import init, Fore
import sys

init(autoreset=True)

def display_banner():
    print(f"{Fore.CYAN}=====================================================")
    print(f"{Fore.CYAN}=          app.wildcard.lol | Auto Tipper           =")
    print(f"{Fore.CYAN}=                 Github: IM-Hanzou                 =")
    print(f"{Fore.CYAN}=====================================================")
    print(f"{Fore.CYAN}= This is free script. Please dont sell this script =")
    print(f"{Fore.CYAN}=              Use it at your own risk              =")
    print(f"{Fore.CYAN}=====================================================")

def get_user_info(bearer_token):
    try:
        url = "https://sys.wildcard.lol/app/my_profile"
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            farcaster_user = data["farcaster_user"]
            key_info = data["key"]
            points_holdings_all = data["points_holdings_all"][0]
            tipping_allowance_24h_all = data["tipping_allowance_24h_all"][0]
            earnings_24h_all = data["earnings_24h_all"][0]
            wallet_list = key_info.get("wallet", [])
            wallet_string = ", ".join(wallet_list) if wallet_list else "N/A"
            
            username = farcaster_user["username"]
            display_name = farcaster_user["display_name"]
            custody_address = farcaster_user["custody_address"]
            
            return username, display_name, custody_address, wallet_string, points_holdings_all, tipping_allowance_24h_all, earnings_24h_all
        else:
            print(f"{Fore.RED}Failed to get user information. Status code: {response.status_code}")
            return None, None, None, None, None, None, None

    except Exception as e:
        print(f"{Fore.RED}Error while getting user information: {str(e)}")
        return None, None, None, None, None, None, None

def display_topics(bearer_token):
    try:
        topics_url = "https://sys.wildcard.lol/app/feed/topics"
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        }

        response = requests.get(topics_url, headers=headers)
        topics = response.json()

        if response.status_code == 200:
            print(f"\n{Fore.YELLOW}List Channel:")
            for i, topic in enumerate(topics, start=1):
                topic_id = topic["id"]
                topic_name = topic["name"]
                print(f"{Fore.GREEN}{i}. {topic_id} | {topic_name}")
            return topics
        else:
            print(f"{Fore.RED}Failed to get channels. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"{Fore.RED}Failed to get channels: {str(e)}")
        return None

def get_channel_info(bearer_token, topics, topic_number, tip_amount):
    try:
        selected_topic = topics[topic_number - 1]
        channel_id = selected_topic["name"]
        channel_url = f"https://sys.wildcard.lol/app/channel/{channel_id}/cast/trending"
        
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        }

        response = requests.get(channel_url, headers=headers)
        if response.status_code == 200:
            channel_data = response.json()
            for item in channel_data:
                farcaster_user = item["farcaster_user"]
                cast_info = item["cast"]
                cast_id = cast_info["id"]
                fid = farcaster_user["fid"]
                
                print(f"\n{Fore.YELLOW}Tipping Cast {channel_id}:")
                print(f"{Fore.MAGENTA}Username: {farcaster_user['username']}")
                print(f"{Fore.MAGENTA}Display Name: {farcaster_user['display_name']}")
                print(f"{Fore.MAGENTA}FID: {fid}")
                print(f"{Fore.CYAN}Cast ID: {cast_id}")
                print(f"{Fore.CYAN}Text: {cast_info['text']}")
                
                tip_success = tip_cast(bearer_token, cast_id, fid, tip_amount)
                if tip_success:
                    print(f"{Fore.GREEN}Success Tip {tip_amount} WILD to {cast_id}")
                    time.sleep(round(random.uniform(1, 5), 2))
                else:
                    print(f"{Fore.RED}Failed Tip to {cast_id}. Your tip Allowance maybe limited.")
                    sys.exit()  
        else:
            print(f"{Fore.RED}Failed to get Casts. Status code: {response.status_code}")
    
    except IndexError:
        print(f"{Fore.RED}No channel selected.")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")

def tip_cast(bearer_token, cast_id, fid, amount):
    try:
        tip_url = f"https://sys.wildcard.lol/app/tip/cast/{cast_id}/{fid}"
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

        response = requests.post(tip_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get("tip") == "success":
                return True
            else:
                return False
        else:
            print(f"{Fore.RED}Failed to tip. Status code: {response.status_code}")
            return False

    except Exception as e:
        print(f"{Fore.RED}Error while tipping: {str(e)}")
        return False

def main():
    display_banner()
    bearer_token = input(f"{Fore.YELLOW}Insert your Bearer token : ")
    
    username, display_name, custody_address, wallet_string, points_holdings_all, tipping_allowance_24h_all, earnings_24h_all = get_user_info(bearer_token)
    if username and display_name:
        print(f"{Fore.MAGENTA}\nUsername: {Fore.CYAN}{username}")
        print(f"{Fore.MAGENTA}Display Name: {Fore.CYAN}{display_name}")
        print(f"{Fore.MAGENTA}Custody Address: {Fore.CYAN}{custody_address}")
        print(f"{Fore.MAGENTA}Wallet: {Fore.CYAN}{wallet_string}")
        print(f"{Fore.MAGENTA}Points Holdings: {Fore.CYAN}{points_holdings_all['display_value']} {points_holdings_all['currency']}")
        print(f"{Fore.MAGENTA}Tipping Allowance 24h: {Fore.CYAN}{tipping_allowance_24h_all['display_value']} {tipping_allowance_24h_all['currency']}")
        print(f"{Fore.MAGENTA}Earnings 24h: {Fore.CYAN}{earnings_24h_all['display_value']} {earnings_24h_all['currency']}")

        topics = display_topics(bearer_token)
        if topics:
            try:
                topic_number = int(input(f"{Fore.BLUE}Insert channel number (insert 0 to tip all casts): "))
                
                if topic_number == 0:
                    tip_amount = float(input(f"{Fore.BLUE}Insert Tip amount: ") or 0)
                    get_ranking_casts_info(bearer_token, tip_amount)
                else:
                    tip_amount = float(input(f"{Fore.BLUE}Insert Tip amount: ") or 0)
                    get_channel_info(bearer_token, topics, topic_number, tip_amount)
                    
            except ValueError:
                print(f"{Fore.RED}Insert a valid number.")
    else:
        print(f"{Fore.RED}Failed to get user information.")

def get_ranking_casts_info(bearer_token, tip_amount):
    try:
        ranking_casts_url = "https://sys.wildcard.lol/app/ranking_casts/trending?source=airstack"
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        }

        response = requests.get(ranking_casts_url, headers=headers)
        if response.status_code == 200:
            ranking_casts_data = response.json()
            for item in ranking_casts_data:
                farcaster_user = item["farcaster_user"]
                cast_info = item["cast"]
                cast_id = cast_info["id"]
                fid = farcaster_user["fid"]
                
                print(f"\n{Fore.YELLOW}Tipping Cast:")
                print(f"{Fore.MAGENTA}Username: {farcaster_user['username']}")
                print(f"{Fore.MAGENTA}Display Name: {farcaster_user['display_name']}")
                print(f"{Fore.MAGENTA}FID: {fid}")
                print(f"{Fore.CYAN}Cast ID: {cast_id}")
                print(f"{Fore.CYAN}Text: {cast_info['text']}")
                
                tip_success = tip_cast(bearer_token, cast_id, fid, tip_amount)
                if tip_success:
                    print(f"{Fore.GREEN}Success Tip {tip_amount} WILD to {cast_id}")
                    time.sleep(round(random.uniform(1, 5), 2))
                else:
                    print(f"{Fore.RED}Failed Tip to {cast_id}. Your tip Allowance maybe limited.")
                    sys.exit()
        else:
            print(f"{Fore.RED}Failed to get casts. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")

if __name__ == "__main__":
    main()
