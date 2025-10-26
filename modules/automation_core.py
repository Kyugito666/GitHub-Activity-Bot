# modules/automation_core.py - Activity Simulation Bot

import logging
import os
import random
import time
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent.parent
LOGIN_URL = "https://github.com/login"

class BrowserError(Exception):
    pass

class ActivityBot:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.current_user = None
        self._setup_browser()
    
    def _setup_browser(self) -> None:
        options = Options()
        
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        
        # Anti-detection basics
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            browser_path = BASE_DIR / "chrome-bin/chrome.exe"
            driver_path = BASE_DIR / "drivers/chromedriver.exe"
            
            if not browser_path.exists() or not driver_path.exists():
                raise BrowserError("Chrome atau ChromeDriver tidak ditemukan")
            
            options.binary_location = str(browser_path)
            service = Service(executable_path=str(driver_path))
            
            logging.info("Starting browser...")
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 30)
            
            if not self.headless:
                self.driver.maximize_window()
            
            # Inject anti-detection
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
            """)
            
            logging.info("✓ Browser ready")
        
        except Exception as e:
            logging.error(f"Browser setup failed: {e}")
            if self.driver:
                self.driver.quit()
            raise BrowserError(str(e))
    
    def _find(self, by: By, value: str, timeout: int = 20) -> Optional[WebElement]:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            logging.warning(f"Element not found: {by}={value}")
            return None
    
    def _click(self, element: WebElement) -> bool:
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(random.uniform(0.2, 0.5))
            
            ActionChains(self.driver).move_to_element(element).pause(
                random.uniform(0.3, 0.7)
            ).click().perform()
            return True
        except:
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                return False
    
    def _type(self, element: WebElement, text: str) -> None:
        self._click(element)
        time.sleep(random.uniform(0.3, 0.6))
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def _delay(self, min_sec: float = 2, max_sec: float = 5) -> None:
        time.sleep(random.uniform(min_sec, max_sec))
    
    def login(self, username: str, password: str) -> bool:
        """Login manual dengan guidance"""
        try:
            logging.info(f"Navigating to login page...")
            self.driver.get(LOGIN_URL)
            
            # Auto-fill credentials
            if username_input := self._find(By.ID, "login_field"):
                self._type(username_input, username)
            
            if password_input := self._find(By.ID, "password"):
                self._type(password_input, password)
            
            if signin_btn := self._find(By.NAME, "commit"):
                self._click(signin_btn)
            
            print("\n" + "="*60)
            print(">>> MANUAL VERIFICATION REQUIRED <<<")
            print("="*60)
            print("1. Selesaikan CAPTCHA/2FA jika muncul")
            print("2. Tunggu hingga dashboard GitHub muncul")
            print("3. Tekan ENTER setelah login berhasil")
            print("="*60)
            input("\nPress ENTER setelah login berhasil: ")
            
            # Verify login
            try:
                self._find(By.CSS_SELECTOR, "img.avatar, summary img", timeout=10)
                self.current_user = username
                logging.info(f"✓ Login successful: {username}")
                return True
            except:
                logging.error("Login verification failed")
                return False
        
        except Exception as e:
            logging.error(f"Login error: {e}")
            return False
    
    def logout(self) -> None:
        try:
            if avatar := self._find(By.CSS_SELECTOR, "summary img[alt*='@']", timeout=5):
                self._click(avatar)
                self._delay(0.5, 1)
                
                if signout := self._find(By.XPATH, "//button[contains(., 'Sign out')]", timeout=5):
                    self._click(signout)
                    logging.info("✓ Logged out")
        except Exception as e:
            logging.warning(f"Logout error: {e}")
        finally:
            self.current_user = None
            try:
                self.driver.delete_all_cookies()
                self.driver.execute_script('sessionStorage.clear();localStorage.clear();')
            except:
                pass
    
    def close(self) -> None:
        if self.driver:
            try:
                self.driver.quit()
                logging.info("Browser closed")
            except:
                pass
    
    # ==================== ACTIVITY METHODS ====================
    
    def create_repository(self, repo_name: str, description: str = "", is_private: bool = False) -> bool:
        """Create new repository"""
        try:
            logging.info(f"Creating repository: {repo_name}")
            self.driver.get("https://github.com/new")
            self._delay(2, 3)
            
            # Repository name
            if name_input := self._find(By.ID, "repository_name"):
                self._type(name_input, repo_name)
                self._delay(1, 2)
            else:
                return False
            
            # Description (optional)
            if description and (desc_input := self._find(By.ID, "repository_description")):
                self._type(desc_input, description)
                self._delay(1, 2)
            
            # Privacy setting
            if is_private:
                if private_radio := self._find(By.ID, "repository_visibility_private"):
                    self._click(private_radio)
                    self._delay(0.5, 1)
            
            # Initialize with README
            if readme_check := self._find(By.ID, "repository_auto_init"):
                if not readme_check.is_selected():
                    self._click(readme_check)
                    self._delay(0.5, 1)
            
            # Submit
            if create_btn := self._find(By.XPATH, "//button[contains(., 'Create repository')]"):
                self._click(create_btn)
                
                # Wait for repo page
                try:
                    self.wait.until(EC.url_contains(f"/{self.current_user}/{repo_name}"))
                    logging.info(f"✓ Repository created: {repo_name}")
                    return True
                except TimeoutException:
                    logging.error("Repository creation timeout")
                    return False
            
            return False
        
        except Exception as e:
            logging.error(f"Create repo error: {e}")
            return False
    
    def star_repository(self, repo_url: str) -> bool:
        """Star a repository"""
        try:
            logging.info(f"Starring: {repo_url}")
            self.driver.get(repo_url)
            self._delay(2, 3)
            
            # Find star button
            star_selectors = [
                "//button[contains(., 'Star')]",
                "//span[contains(text(), 'Star')]//ancestor::button"
            ]
            
            for selector in star_selectors:
                try:
                    if star_btn := self.driver.find_element(By.XPATH, selector):
                        if star_btn.is_displayed() and "Unstar" not in star_btn.text:
                            self._click(star_btn)
                            self._delay(1, 2)
                            logging.info("✓ Repository starred")
                            return True
                except NoSuchElementException:
                    continue
            
            logging.warning("Already starred or button not found")
            return False
        
        except Exception as e:
            logging.error(f"Star error: {e}")
            return False
    
    def follow_user(self, username: str) -> bool:
        """Follow a user"""
        try:
            logging.info(f"Following user: {username}")
            self.driver.get(f"https://github.com/{username}")
            self._delay(2, 3)
            
            # Find follow button
            if follow_btn := self._find(By.XPATH, "//button[contains(., 'Follow')]", timeout=5):
                if "Unfollow" not in follow_btn.text:
                    self._click(follow_btn)
                    self._delay(1, 2)
                    logging.info(f"✓ Followed: {username}")
                    return True
                else:
                    logging.warning(f"Already following {username}")
                    return False
            
            logging.error("Follow button not found")
            return False
        
        except Exception as e:
            logging.error(f"Follow error: {e}")
            return False
    
    def browse_trending(self, duration_seconds: int = 30) -> None:
        """Browse trending repositories (human-like)"""
        try:
            logging.info("Browsing trending repositories...")
            self.driver.get("https://github.com/trending")
            self._delay(3, 5)
            
            start_time = time.time()
            scroll_count = 0
            
            while time.time() - start_time < duration_seconds:
                # Random scroll
                scroll_amount = random.randint(300, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                self._delay(2, 4)
                
                scroll_count += 1
                
                # Occasionally scroll up (realistic behavior)
                if scroll_count % 3 == 0:
                    self.driver.execute_script(f"window.scrollBy(0, -{random.randint(100, 300)});")
                    self._delay(1, 2)
                
                # Random click on repo (view details)
                if random.random() < 0.3:  # 30% chance
                    try:
                        repos = self.driver.find_elements(By.CSS_SELECTOR, "article h2 a")
                        if repos:
                            random.choice(repos).click()
                            self._delay(3, 6)
                            self.driver.back()
                            self._delay(2, 3)
                    except:
                        pass
            
            logging.info(f"✓ Browsed trending for {duration_seconds}s")
        
        except Exception as e:
            logging.error(f"Browse error: {e}")
    
    def commit_file(self, repo_name: str, file_name: str, file_content: str, commit_msg: str) -> bool:
        """Add/commit file to repository"""
        try:
            logging.info(f"Committing file: {file_name} to {repo_name}")
            
            # Navigate to repo
            self.driver.get(f"https://github.com/{self.current_user}/{repo_name}")
            self._delay(2, 3)
            
            # Click "Add file" dropdown
            if add_file := self._find(By.CSS_SELECTOR, "summary[aria-label='Add file']", timeout=10):
                self._click(add_file)
                self._delay(0.5, 1)
            else:
                logging.error("Add file button not found")
                return False
            
            # Click "Create new file"
            if create_new := self._find(By.XPATH, "//span[contains(text(), 'Create new file')]"):
                self._click(create_new)
                self._delay(2, 3)
            else:
                return False
            
            # File name
            if name_input := self._find(By.CSS_SELECTOR, "input[name='filename']"):
                self._type(name_input, file_name)
                self._delay(1, 2)
            else:
                return False
            
            # File content (CodeMirror editor)
            if content_area := self._find(By.CSS_SELECTOR, ".CodeMirror textarea"):
                content_area.send_keys(file_content)
                self._delay(2, 3)
            else:
                return False
            
            # Commit message (optional, use default if not provided)
            if commit_msg:
                if msg_input := self._find(By.ID, "commit-summary-input"):
                    msg_input.clear()
                    self._type(msg_input, commit_msg)
                    self._delay(1, 2)
            
            # Commit button
            if commit_btn := self._find(By.XPATH, "//button[contains(., 'Commit new file') or contains(., 'Commit changes')]"):
                self._click(commit_btn)
                
                # Wait for file page
                self._delay(3, 5)
                logging.info(f"✓ File committed: {file_name}")
                return True
            
            return False
        
        except Exception as e:
            logging.error(f"Commit error: {e}")
            return False
    
    def explore_topics(self, topic: str, duration_seconds: int = 20) -> None:
        """Explore specific topic"""
        try:
            logging.info(f"Exploring topic: {topic}")
            self.driver.get(f"https://github.com/topics/{topic}")
            self._delay(3, 5)
            
            start_time = time.time()
            
            while time.time() - start_time < duration_seconds:
                # Scroll
                self.driver.execute_script(f"window.scrollBy(0, {random.randint(300, 600)});")
                self._delay(2, 4)
                
                # Random repo click
                if random.random() < 0.4:
                    try:
                        repos = self.driver.find_elements(By.CSS_SELECTOR, "article h3 a")
                        if repos:
                            random.choice(repos).click()
                            self._delay(4, 7)
                            self.driver.back()
                            self._delay(2, 3)
                    except:
                        pass
            
            logging.info(f"✓ Explored topic: {topic}")
        
        except Exception as e:
            logging.error(f"Explore error: {e}")