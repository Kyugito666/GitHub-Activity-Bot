# modules/multi_account.py - Multi-Account Orchestrator

import logging
import random
import time
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime

from .automation_core import ActivityBot, BrowserError
from . import tasks

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEDULE_FILE = BASE_DIR / "data/schedule.txt"

class MultiAccountManager:
    def __init__(self, accounts: List[Tuple[str, str]]):
        self.accounts = accounts
        self.execution_log = []
        self.current_bot = None
    
    def _log_execution(self, username: str, activity: str, status: str) -> None:
        """Log execution untuk tracking"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {username} | {activity} | {status}"
        self.execution_log.append(log_entry)
        
        # Save to file
        SCHEDULE_FILE.parent.mkdir(exist_ok=True)
        with open(SCHEDULE_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def _get_last_activity_time(self, username: str) -> Optional[float]:
        """Get timestamp of last activity for this account"""
        if not SCHEDULE_FILE.exists():
            return None
        
        try:
            with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in reversed(lines):
                if username in line and "SUCCESS" in line:
                    # Parse timestamp
                    timestamp_str = line.split('|')[0].strip()
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    return dt.timestamp()
            
            return None
        except Exception as e:
            logging.warning(f"Failed to read schedule: {e}")
            return None
    
    def _calculate_delay(self, username: str, min_hours: float = 6) -> int:
        """Calculate delay needed before next activity"""
        last_time = self._get_last_activity_time(username)
        
        if not last_time:
            return 0  # No previous activity, can run now
        
        elapsed = time.time() - last_time
        min_seconds = min_hours * 3600
        
        if elapsed >= min_seconds:
            return 0
        
        return int(min_seconds - elapsed)
    
    def run_sequential(self, headless: bool = False, 
                      activity_type: str = "daily", 
                      delay_between: int = 300) -> None:
        """
        Run activities sequentially across all accounts
        
        Args:
            headless: Run in headless mode
            activity_type: "daily", "browse", "create_repo", "marathon"
            delay_between: Delay between accounts (seconds)
        """
        print("\n" + "="*70)
        print("       MULTI-ACCOUNT SEQUENTIAL MODE")
        print("="*70)
        print(f"Accounts: {len(self.accounts)}")
        print(f"Activity: {activity_type}")
        print(f"Delay between accounts: {delay_between}s ({delay_between//60}min)")
        print(f"Estimated total time: {(len(self.accounts) * delay_between)//60}min")
        print("="*70)
        
        confirm = input("\nStart sequential execution? (y/n): ").lower()
        if confirm != 'y':
            return
        
        for idx, (username, password) in enumerate(self.accounts, 1):
            print(f"\n{'='*70}")
            print(f"ACCOUNT {idx}/{len(self.accounts)}: {username}")
            print(f"{'='*70}")
            
            # Check if account needs cooldown
            delay_needed = self._calculate_delay(username, min_hours=6)
            if delay_needed > 0:
                print(f"⏳ Account on cooldown: {delay_needed//3600}h {(delay_needed%3600)//60}m remaining")
                print("Skipping to next account...")
                continue
            
            try:
                # Initialize bot
                print(f"\n[{idx}] Initializing browser...")
                self.current_bot = ActivityBot(headless=headless)
                
                # Login
                print(f"[{idx}] Logging in...")
                if not self.current_bot.login(username, password):
                    print(f"✗ Login failed for {username}")
                    self._log_execution(username, activity_type, "LOGIN_FAILED")
                    self.current_bot.close()
                    continue
                
                print(f"✓ Logged in: {username}")
                
                # Execute activity
                print(f"[{idx}] Executing activity: {activity_type}")
                success = self._execute_activity(activity_type)
                
                status = "SUCCESS" if success else "FAILED"
                self._log_execution(username, activity_type, status)
                
                if success:
                    print(f"✓ Activity completed: {username}")
                else:
                    print(f"✗ Activity failed: {username}")
                
                # Logout & cleanup
                print(f"[{idx}] Logging out...")
                self.current_bot.logout()
                self.current_bot.close()
                self.current_bot = None
                
                # Delay before next account (except last)
                if idx < len(self.accounts):
                    print(f"\n⏳ Waiting {delay_between}s before next account...")
                    time.sleep(delay_between)
            
            except BrowserError as e:
                print(f"✗ Browser error for {username}: {e}")
                self._log_execution(username, activity_type, "BROWSER_ERROR")
                if self.current_bot:
                    self.current_bot.close()
                    self.current_bot = None
            
            except KeyboardInterrupt:
                print(f"\n>>> Interrupted at account {idx}")
                if self.current_bot:
                    self.current_bot.close()
                break
            
            except Exception as e:
                logging.error(f"Unexpected error for {username}: {e}", exc_info=True)
                self._log_execution(username, activity_type, "ERROR")
                if self.current_bot:
                    self.current_bot.close()
                    self.current_bot = None
        
        # Summary
        print("\n" + "="*70)
        print("       EXECUTION SUMMARY")
        print("="*70)
        success_count = sum(1 for log in self.execution_log if "SUCCESS" in log)
        print(f"Total accounts: {len(self.accounts)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {len(self.accounts) - success_count}")
        print("="*70)
    
    def run_round_robin(self, headless: bool = False,
                       rounds: int = 3,
                       delay_between_rounds: int = 7200) -> None:
        """
        Run multiple rounds with all accounts (untuk daily maintenance)
        
        Args:
            headless: Run in headless mode
            rounds: Number of rounds to execute
            delay_between_rounds: Delay between rounds (default 2 hours)
        """
        print("\n" + "="*70)
        print("       MULTI-ACCOUNT ROUND-ROBIN MODE")
        print("="*70)
        print(f"Accounts: {len(self.accounts)}")
        print(f"Rounds: {rounds}")
        print(f"Delay between rounds: {delay_between_rounds//3600}h")
        print(f"Total duration: ~{(rounds * delay_between_rounds)//3600}h")
        print("="*70)
        
        confirm = input("\nStart round-robin execution? (y/n): ").lower()
        if confirm != 'y':
            return
        
        for round_num in range(1, rounds + 1):
            print(f"\n{'#'*70}")
            print(f"# ROUND {round_num}/{rounds}")
            print(f"{'#'*70}")
            
            # Run all accounts
            self.run_sequential(
                headless=headless,
                activity_type="daily",
                delay_between=random.randint(180, 420)  # 3-7 min
            )
            
            # Delay before next round (except last)
            if round_num < rounds:
                print(f"\n⏳ Round {round_num} completed. Waiting {delay_between_rounds//3600}h before round {round_num + 1}...")
                time.sleep(delay_between_rounds)
        
        print("\n" + "="*70)
        print("✓ ROUND-ROBIN COMPLETED")
        print("="*70)
    
    def run_smart_schedule(self, headless: bool = False,
                          sessions_per_day: int = 2,
                          activity_mix: bool = True) -> None:
        """
        Smart scheduling dengan cooldown & activity variety
        Runs continuously, respecting cooldowns
        
        Args:
            headless: Run in headless mode
            sessions_per_day: Target sessions per account per day
            activity_mix: Mix different activity types
        """
        print("\n" + "="*70)
        print("       SMART SCHEDULE MODE (24/7 Ready)")
        print("="*70)
        print(f"Accounts: {len(self.accounts)}")
        print(f"Target: {sessions_per_day} sessions/account/day")
        print(f"Activity mix: {'Enabled' if activity_mix else 'Daily Set Only'}")
        print(f"Cooldown: 6 hours between sessions per account")
        print("="*70)
        print("\nThis mode will run continuously until interrupted.")
        print("Press Ctrl+C to stop gracefully.")
        
        confirm = input("\nStart smart schedule? (y/n): ").lower()
        if confirm != 'y':
            return
        
        activity_types = ["daily", "browse", "create_repo"] if activity_mix else ["daily"]
        
        try:
            while True:
                print(f"\n{'='*70}")
                print(f"Checking accounts at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*70}")
                
                # Check each account
                accounts_ready = []
                for username, password in self.accounts:
                    delay_needed = self._calculate_delay(username, min_hours=6)
                    if delay_needed == 0:
                        accounts_ready.append((username, password))
                    else:
                        hours = delay_needed // 3600
                        mins = (delay_needed % 3600) // 60
                        print(f"⏳ {username}: cooldown {hours}h {mins}m")
                
                if not accounts_ready:
                    print("\n⏸️  No accounts ready. Checking again in 30 minutes...")
                    time.sleep(1800)
                    continue
                
                print(f"\n✓ {len(accounts_ready)} accounts ready for activity")
                
                # Execute ready accounts
                for username, password in accounts_ready:
                    activity = random.choice(activity_types)
                    
                    print(f"\n--- Processing: {username} ({activity}) ---")
                    
                    try:
                        self.current_bot = ActivityBot(headless=headless)
                        
                        if self.current_bot.login(username, password):
                            success = self._execute_activity(activity)
                            status = "SUCCESS" if success else "FAILED"
                            self._log_execution(username, activity, status)
                            
                            self.current_bot.logout()
                        else:
                            self._log_execution(username, activity, "LOGIN_FAILED")
                        
                        self.current_bot.close()
                        self.current_bot = None
                        
                        # Random delay between accounts
                        delay = random.randint(180, 420)
                        print(f"⏳ Waiting {delay}s before next account...")
                        time.sleep(delay)
                    
                    except Exception as e:
                        logging.error(f"Error for {username}: {e}")
                        if self.current_bot:
                            self.current_bot.close()
                            self.current_bot = None
                
                # Check again in 30 minutes
                print(f"\n✓ Cycle completed. Next check in 30 minutes...")
                time.sleep(1800)
        
        except KeyboardInterrupt:
            print("\n>>> Smart schedule stopped")
            if self.current_bot:
                self.current_bot.close()
    
    def _execute_activity(self, activity_type: str) -> bool:
        """Execute specific activity type"""
        try:
            if activity_type == "daily":
                tasks.task_daily_activity(self.current_bot)
                return True
            
            elif activity_type == "browse":
                self.current_bot.browse_trending(duration_seconds=random.randint(30, 60))
                return True
            
            elif activity_type == "create_repo":
                tasks.task_create_repo(self.current_bot)
                return True
            
            elif activity_type == "marathon":
                tasks.task_marathon_mode(self.current_bot)
                return True
            
            else:
                logging.error(f"Unknown activity type: {activity_type}")
                return False
        
        except Exception as e:
            logging.error(f"Activity execution error: {e}")
            return False
    
    def show_schedule_status(self) -> None:
        """Display schedule status for all accounts"""
        print("\n" + "="*70)
        print("       ACCOUNT SCHEDULE STATUS")
        print("="*70)
        print(f"{'Account':<20} {'Last Activity':<20} {'Cooldown':<15} {'Status'}")
        print("-"*70)
        
        for username, _ in self.accounts:
            last_time = self._get_last_activity_time(username)
            
            if not last_time:
                print(f"{username:<20} {'Never':<20} {'N/A':<15} {'Ready'}")
                continue
            
            last_dt = datetime.fromtimestamp(last_time)
            last_str = last_dt.strftime("%Y-%m-%d %H:%M")
            
            delay_needed = self._calculate_delay(username, min_hours=6)
            
            if delay_needed == 0:
                cooldown_str = "Ready"
                status = "✓ Ready"
            else:
                hours = delay_needed // 3600
                mins = (delay_needed % 3600) // 60
                cooldown_str = f"{hours}h {mins}m"
                status = "⏳ Cooldown"
            
            print(f"{username:<20} {last_str:<20} {cooldown_str:<15} {status}")
        
        print("="*70)