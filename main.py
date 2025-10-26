# main.py - GitHub Activity Bot

import logging
import random
from pathlib import Path

from modules.automation_core import ActivityBot, BrowserError
def display_main_menu() -> str:
    """Display main menu"""
    print("\n" + "="*60)
    print("          GITHUB ACTIVITY BOT - MAIN MENU")
    print("="*60)
    print("--- SINGLE ACCOUNT MODE ---")
    print("1. Login ke Akun GitHub")
    print("2. Jalankan Aktivitas")
    print("3. Logout")
    print("")
    print("--- MULTI ACCOUNT MODE ---")
    print("4. Multi-Account Sequential")
    print("5. Multi-Account Round-Robin")
    print("6. Multi-Account Smart Schedule (24/7)")
    print("7. Show Schedule Status")
    print("")
    print("0. Exit")
    print("-"*60)
    return input(">>> Pilihan: ").strip()

def ask_headless_mode() -> bool:
    """Ask for headless mode"""
    choice = input(">>> Jalankan headless mode? (y/n): ").lower().strip()
    return choice == 'y'

BASE_DIR = Path(__file__).resolve().parent
ACCOUNTS_FILE = BASE_DIR / "data/accounts.txt"
LOG_FILE = BASE_DIR / "logs/activity.log"

LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def load_accounts() -> list:
    """Load accounts dari file (format: username:password)"""
    if not ACCOUNTS_FILE.exists():
        logging.warning(f"File {ACCOUNTS_FILE} tidak ditemukan")
        ACCOUNTS_FILE.parent.mkdir(exist_ok=True)
        ACCOUNTS_FILE.write_text("# Format: username:password\n# Example: myuser:mypassword123\n")
        return []
    
    accounts = []
    with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if ':' in line:
                    username, password = line.split(':', 1)
                    accounts.append((username.strip(), password.strip()))
    
    return accounts

def main_controller():
    bot = None
    
    try:
        while True:
            choice = display_main_menu()
            
            if choice == '1':
                # SINGLE ACCOUNT LOGIN
                if bot:
                    print(">>> Sudah login. Logout dulu (pilihan 3)")
                    continue
                
                accounts = load_accounts()
                if not accounts:
                    print(f">>> Tidak ada akun di {ACCOUNTS_FILE}")
                    print(">>> Tambahkan akun dengan format: username:password")
                    continue
                
                print(f"\n>>> Ditemukan {len(accounts)} akun")
                print("1. Pilih akun manual")
                print("2. Random akun")
                
                sub = input(">>> Pilihan: ").strip()
                
                if sub == '1':
                    for idx, (user, _) in enumerate(accounts, 1):
                        print(f"{idx}. {user}")
                    
                    try:
                        acc_idx = int(input(">>> Nomor akun: ")) - 1
                        username, password = accounts[acc_idx]
                    except:
                        print(">>> Pilihan invalid")
                        continue
                
                elif sub == '2':
                    username, password = random.choice(accounts)
                    print(f">>> Selected: {username}")
                else:
                    continue
                
                headless = ask_headless_mode()
                
                try:
                    bot = ActivityBot(headless=headless)
                    
                    if bot.login(username, password):
                        print(f"✓ Login berhasil: {username}")
                    else:
                        print("✗ Login gagal")
                        bot.close()
                        bot = None
                
                except BrowserError as e:
                    print(f"✗ Browser error: {e}")
                    bot = None
            
            elif choice == '2':
                # SINGLE ACCOUNT ACTIVITIES
                if not bot:
                    print(">>> Harap login dulu (pilihan 1)")
                    continue
                
                tasks.activity_menu(bot)
            
            elif choice == '3':
                # SINGLE ACCOUNT LOGOUT
                if not bot:
                    print(">>> Belum login")
                    continue
                
                bot.logout()
                bot.close()
                bot = None
                print("✓ Logout berhasil")
            
            elif choice == '4':
                # MULTI-ACCOUNT SEQUENTIAL
                if bot:
                    print(">>> Logout dari single account dulu (pilihan 3)")
                    continue
                
                accounts = load_accounts()
                if len(accounts) < 2:
                    print(">>> Minimal 2 akun untuk multi-account mode")
                    continue
                
                print("\n--- MULTI-ACCOUNT SEQUENTIAL SETUP ---")
                print("Activity types:")
                print("1. Daily Activity Set (Recommended)")
                print("2. Browse Only")
                print("3. Create Repository")
                print("4. Marathon Mode (1 hour)")
                
                activity_choice = input(">>> Pilih activity: ").strip()
                activity_map = {"1": "daily", "2": "browse", "3": "create_repo", "4": "marathon"}
                activity_type = activity_map.get(activity_choice, "daily")
                
                delay = int(input(">>> Delay antar akun (detik, default 300): ") or "300")
                headless = ask_headless_mode()
                
                manager = MultiAccountManager(accounts)
                manager.run_sequential(
                    headless=headless,
                    activity_type=activity_type,
                    delay_between=delay
                )
            
            elif choice == '5':
                # MULTI-ACCOUNT ROUND-ROBIN
                if bot:
                    print(">>> Logout dari single account dulu")
                    continue
                
                accounts = load_accounts()
                if len(accounts) < 2:
                    print(">>> Minimal 2 akun")
                    continue
                
                print("\n--- ROUND-ROBIN SETUP ---")
                rounds = int(input(">>> Jumlah rounds (default 3): ") or "3")
                delay_hours = int(input(">>> Delay antar rounds (jam, default 2): ") or "2")
                headless = ask_headless_mode()
                
                manager = MultiAccountManager(accounts)
                manager.run_round_robin(
                    headless=headless,
                    rounds=rounds,
                    delay_between_rounds=delay_hours * 3600
                )
            
            elif choice == '6':
                # MULTI-ACCOUNT SMART SCHEDULE
                if bot:
                    print(">>> Logout dari single account dulu")
                    continue
                
                accounts = load_accounts()
                if len(accounts) < 2:
                    print(">>> Minimal 2 akun")
                    continue
                
                print("\n--- SMART SCHEDULE SETUP ---")
                print("This mode runs 24/7 with automatic cooldown management")
                sessions = int(input(">>> Target sessions/account/day (default 2): ") or "2")
                mix = input(">>> Mix activity types? (y/n, default y): ").lower() != 'n'
                headless = ask_headless_mode()
                
                manager = MultiAccountManager(accounts)
                manager.run_smart_schedule(
                    headless=headless,
                    sessions_per_day=sessions,
                    activity_mix=mix
                )
            
            elif choice == '7':
                # SHOW SCHEDULE STATUS
                accounts = load_accounts()
                if not accounts:
                    print(">>> Tidak ada akun")
                    continue
                
                manager = MultiAccountManager(accounts)
                manager.show_schedule_status()
            
            elif choice == '0':
                # EXIT
                if bot:
                    bot.close()
                logging.info("Program terminated")
                break
            
            else:
                print(">>> Pilihan tidak valid")
    
    except KeyboardInterrupt:
        print("\n>>> Interrupted")
        if bot:
            bot.close()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        if bot:
            bot.close()

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║         GitHub Activity Bot - Anti-Flag System           ║
║                   Simulate Human Behavior                ║
╚══════════════════════════════════════════════════════════╝
    """)
    main_controller()