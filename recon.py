import socket
import requests
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

init(autoreset=True)

def banner():
    print(Fore.GREEN + """
    ███╗   ███╗ █████╗ ██╗  ██╗ █████╗ ███████╗███╗   ██╗██╗  ██╗███████╗
    ████╗ ████║██╔══██╗██║  ██║██╔══██╗██╔════╝████╗  ██║██║  ██║██╔════╝
    ██╔████╔██║███████║███████║███████║███████╗██╔██╗ ██║███████║█████╗  
    ██║╚██╔╝██║██╔══██║██╔══██║██╔══██║╚════██║██║╚██╗██║██╔══██║██╔══╝  
    ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██║███████║██║ ╚██╗██║██║  ██║███████╗
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚██═╝╚═╝  ╚═╝╚══════╝
            [ Al-Mahasneh Cyber Recon & Port Scanner v2.0 ]
            [        Coded for Elite Cyber Portfolio      ]
    """)

def check_port(target_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    result = s.connect_ex((target_ip, port))
    s.close()
    if result == 0:
        print(Fore.GREEN + f"    [OPEN]   Port {port:<5} is active.")

def scan_target(target):
    clean_target = target.replace("http://", "").replace("https://", "").strip("/")
    try:
        target_ip = socket.gethostbyname(clean_target)
    except socket.gaierror:
        print(Fore.RED + f"[-] Error: Unable to resolve hostname '{clean_target}'.")
        return

    print(Fore.YELLOW + f"\n[*] Target Acquired: {clean_target} ({target_ip})")
    print(Fore.YELLOW + f"[*] Scan Initialized at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(Fore.YELLOW + "[*] Performing HTTP Reconnaissance...")
    try:
        url = f"http://{clean_target}"
        response = requests.get(url, timeout=3)
        print(Fore.CYAN + f"[+] Web Service Online (HTTP Status: {response.status_code})")
        print(Fore.CYAN + f"[+] Server Header: {response.headers.get('Server', 'Hidden/Unknown')}")
    except requests.exceptions.RequestException:
        print(Fore.RED + "[-] Web Service Offline or Unreachable on Port 80.")

    ports_to_check = [21, 22, 25, 53, 80, 110, 443, 3306, 8080, 8443]
    print(Fore.YELLOW + f"\n[*] Fast-Scanning {len(ports_to_check)} Critical Ports...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        for port in ports_to_check:
            executor.submit(check_port, target_ip, port)

    print(Fore.GREEN + "\n[+] Reconnaissance Complete. Stay Safe, Stay Ethical.")

if __name__ == "__main__":
    banner()
    try:
        target_input = input(Fore.WHITE + "Enter Target IP or Domain (e.g., scanme.nmap.org): ")
        if target_input:
            scan_target(target_input)
        else:
            print(Fore.RED + "[-] Error: Target cannot be empty.")
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[-] Scan cancelled by user. Exiting...")
        sys.exit()
