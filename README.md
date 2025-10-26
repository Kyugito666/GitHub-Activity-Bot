\# GitHub Activity Bot



🤖 Automated GitHub activity simulator dengan multi-account support dan AI-powered content generation. Anti-flag system untuk maintain natural behavior patterns.



\## ✨ Features



\- 🔐 \*\*Multi-Account Management\*\* - Sequential, Round-Robin, dan Smart Schedule modes

\- 🧠 \*\*AI Content Generation\*\* - Repository names, files, dan commit messages via Gemini

\- 🛡️ \*\*Anti-Flag System\*\* - Cooldown management, random delays, activity variety

\- 📊 \*\*Activity Tracking\*\* - Execution logs dan schedule monitoring

\- 🎯 \*\*7 Activity Types\*\* - Create repo, star, follow, browse, commit, daily set, marathon

\- ⚡ \*\*Headless Mode\*\* - Background execution support

\- 🔄 \*\*24/7 Operation\*\* - Smart schedule dengan automatic cooldown



\## 🚀 Quick Start



\### 1. Install

```bash

pip install -r requirements.txt

```



\### 2. Setup Accounts

```bash

\# Create accounts file

cat > data/accounts.txt << EOF

your\_username:your\_password

another\_user:another\_pass

EOF

```



\### 3. Configure API (Optional)

```bash

\# Edit .env

GEMINI\_API\_KEY="your\_api\_key\_here"

```



\### 4. Run

```bash

python main.py

```



\## 📖 Usage



\### Single Account Mode

```

1\. Login          → Pilih akun, solve CAPTCHA manual

2\. Activities     → Menu 7 aktivitas tersedia

3\. Logout         → Clean session \& cookies

```



\### Multi-Account Mode

```

4\. Sequential       → Run all accounts one by one

5\. Round-Robin      → Multiple rounds with delays

6\. Smart Schedule   → 24/7 auto with cooldown (6h between sessions)

7\. Status           → Check cooldown \& last activity

```



\## 🎯 Activity Types



| Activity | Duration | Risk | Description |

|----------|----------|------|-------------|

| \*\*Daily Activity Set\*\* ⭐ | 5-10 min | Low | Browse + Explore + Star + Follow |

| Create Repository | 3-5 min | Medium | AI-generated repo with files |

| Star Trending | 30 sec | Low | Star popular repos |

| Follow User | 30 sec | Low | Follow popular developers |

| Browse \& Explore | 20-60 sec | Very Low | Human-like scrolling |

| Commit File | 2-3 min | Medium | Add AI-generated file |

| Marathon Mode | 60 min | High | 1 hour continuous activity |



\## 📊 Multi-Account Modes



\### Sequential

Run all accounts once, one after another.

```

Account 1 → Activity → Delay → Account 2 → Activity → Delay → Account 3

```

\*\*Use:\*\* Morning/evening batch processing



\### Round-Robin

Multiple rounds with delays between rounds.

```

Round 1: All accounts → 2h delay → Round 2: All accounts → Done

```

\*\*Use:\*\* Spread activities across day



\### Smart Schedule (24/7)

Automatic execution with 6-hour cooldown per account.

```

Loop:

&nbsp; Check ready accounts → Process → Wait 30 min → Repeat

```

\*\*Use:\*\* Set and forget automation



\## 🛡️ Anti-Flag Strategy



\### Cooldown System

\- \*\*6 hours minimum\*\* between sessions per account

\- \*\*Random delays\*\* (2-10 min) between activities

\- \*\*Activity variety\*\* prevents pattern detection



\### Recommended Schedule

```

Morning (09:00):   Daily Activity Set (all accounts)

Afternoon (14:00): Browse Only (random accounts)

Evening (20:00):   Create Repo (2-3 accounts max)

```



\### Safety Limits

\- ✅ \*\*3-5 accounts\*\* per IP recommended

\- ✅ \*\*2-3 sessions\*\* per account per day

\- ✅ \*\*1-2 repos\*\* created per week per account

\- ❌ Avoid marathon mode on new accounts (<30 days)



\## 📁 Project Structure



```

github/

├── modules/

│   ├── automation\_core.py      # Bot core (Selenium)

│   ├── multi\_account.py        # Multi-account orchestrator

│   ├── ai\_core.py              # AI integration (Gemini)

│   └── tasks.py                # Activity tasks

├── data/

│   ├── accounts.txt            # Accounts (username:password)

│   └── schedule.txt            # Execution log (auto-generated)

├── logs/

│   └── activity.log            # Detailed logs

├── chrome-bin/

│   └── chrome.exe              # Chrome binary

├── drivers/

│   └── chromedriver.exe        # ChromeDriver

├── main.py                     # Entry point

├── .env                        # Gemini API key

└── requirements.txt

```



\## 🔧 Configuration



\### Headless Mode

```python

\# Show browser (debugging)

Headless: n



\# Background (production)

Headless: y

```



\### Cooldown Time

Edit `multi\_account.py`:

```python

delay\_needed = self.\_calculate\_delay(username, min\_hours=6)  # Change 6 to desired hours

```



\### Activity Mix

Smart Schedule supports mixed activities:

```python

activity\_types = \["daily", "browse", "create\_repo"]  # Add/remove types

```



\## 📊 Monitoring



\### Check Status

```bash

python main.py

\# Menu: 7 (Show Schedule Status)

```



\### Watch Logs

```bash

tail -f logs/activity.log

```



\### Execution History

```bash

cat data/schedule.txt

```



\## ⚠️ Important Notes



\### Manual Verification Required

\- CAPTCHA solving during login

\- 2FA codes if enabled

\- Bot will pause and wait for ENTER



\### Rate Limits

\- \*\*60 API requests/hour\*\* (GitHub unauthenticated)

\- \*\*Max 5-10 accounts\*\* per IP per day (safe limit)

\- \*\*Temporary bans\*\* possible if exceeded (1-6 hours)



\### Account Safety

\- Use test accounts for initial testing

\- Never commit `accounts.txt` to repository

\- Consider using environment variables in production



\## 🐛 Troubleshooting



\### Browser Won't Open

```bash

\# Check paths

ls chrome-bin/chrome.exe

ls drivers/chromedriver.exe



\# Verify versions match

chrome.exe --version

chromedriver.exe --version

```



\### Login Failed

```bash

\# Test credentials manually

\# Open Chrome → github.com/login

\# Use same credentials from accounts.txt



\# Check for rate limiting

\# Wait 15-30 minutes and retry

```



\### Activities Failing

```bash

\# Run with visible browser

Headless: n



\# Check detailed logs

grep "ERROR" logs/activity.log | tail -20



\# Update Chrome/Driver if outdated

```



\## 🎓 Examples



\### Example 1: Conservative Daily

```bash

python main.py

\# Menu: 6 (Smart Schedule)

\# Sessions: 2

\# Mix: y

\# Headless: y

\# Let it run 24/7

```



\### Example 2: Morning Batch

```bash

python main.py

\# Menu: 4 (Sequential)

\# Activity: 1 (Daily Set)

\# Delay: 300

\# Headless: y

```



\### Example 3: Weekend Boost

```bash

python main.py

\# Menu: 5 (Round-Robin)

\# Rounds: 3

\# Delay: 4

\# Headless: n

```



\## 📦 Dependencies



```

selenium==4.22.0

google-generativeai==0.7.1

python-dotenv==1.0.1

```



\## 🤝 Best Practices



1\. \*\*Start Small\*\* - Test with 1-2 accounts first

2\. \*\*Monitor Logs\*\* - Check daily for errors

3\. \*\*Vary Activities\*\* - Don't repeat same pattern

4\. \*\*Respect Cooldowns\*\* - Let accounts rest

5\. \*\*Use Headless\*\* - Save resources in production

6\. \*\*Backup Data\*\* - Keep accounts.txt secure



\## 📈 Success Metrics



\### Healthy Account

\- ✅ 80%+ schedule completion rate

\- ✅ No LOGIN\_FAILED in 24h

\- ✅ Mixed activity types

\- ✅ Consistent daily execution



\### Warning Signs

\- ⚠️ Multiple LOGIN\_FAILED

\- ⚠️ CAPTCHA every login

\- ⚠️ Activities timing out



\## 🔒 Security



\- Credentials stored in plain text (`accounts.txt`) - use at own risk

\- No password encryption by default

\- Recommended: Use dedicated test accounts

\- Production: Consider environment variables or secrets management



\## 📄 License



MIT License - Use at your own risk. Automating GitHub activities may violate their Terms of Service.



\## ⚠️ Disclaimer



This tool is for educational purposes. Automated activity on GitHub may result in account suspension. Use responsibly and at your own risk.



---



\*\*Version:\*\* 2.0.0  

\*\*Status:\*\* Production Ready  

\*\*Last Updated:\*\* 2025-10-11

