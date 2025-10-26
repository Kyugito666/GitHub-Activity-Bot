# modules/tasks.py - Activity Tasks with AI Integration

import logging
import random
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .automation_core import ActivityBot

from . import ai_core

def activity_menu(bot: 'ActivityBot') -> None:
    """Main activity menu"""
    while True:
        print("\n" + "="*60)
        print("           GITHUB ACTIVITY MENU")
        print("="*60)
        print("1. Create Repository (dengan AI content)")
        print("2. Star Random Trending Repo")
        print("3. Follow Random User")
        print("4. Browse & Explore (Human-like)")
        print("5. Commit File ke Repository")
        print("6. Complete Daily Activity Set (Recommended)")
        print("7. Marathon Mode (1 jam aktivitas random)")
        print("9. Back to Main Menu")
        print("-"*60)
        
        choice = input(">>> Pilihan: ").strip()
        
        if choice == '1':
            task_create_repo(bot)
        elif choice == '2':
            task_star_trending(bot)
        elif choice == '3':
            task_follow_user(bot)
        elif choice == '4':
            task_browse_explore(bot)
        elif choice == '5':
            task_commit_file(bot)
        elif choice == '6':
            task_daily_activity(bot)
        elif choice == '7':
            task_marathon_mode(bot)
        elif choice == '9':
            print(">>> Kembali ke menu utama")
            break
        else:
            print(">>> Pilihan tidak valid")

def task_create_repo(bot: 'ActivityBot') -> None:
    """Create repository dengan konten dari AI"""
    print("\n--- CREATE REPOSITORY ---")
    
    # Generate nama repo dari AI
    repo_data = ai_core.generate_repo_name()
    if not repo_data:
        print("✗ AI gagal generate repo name")
        return
    
    repo_name = repo_data.get("repo_name", f"project-{int(time.time())}")
    description = repo_data.get("description", "")
    
    print(f"AI Generated:")
    print(f"  Name: {repo_name}")
    print(f"  Desc: {description}")
    
    confirm = input("\nLanjutkan? (y/n): ").lower()
    if confirm != 'y':
        return
    
    if bot.create_repository(repo_name, description):
        print(f"✓ Repository created: {repo_name}")
        
        # Add initial file
        time.sleep(random.uniform(3, 6))
        
        file_data = ai_core.generate_file_content(repo_name)
        if file_data:
            filename = file_data.get("filename")
            content = file_data.get("content")
            
            print(f"\nAdding file: {filename}")
            if bot.commit_file(repo_name, filename, content, f"Add {filename}"):
                print(f"✓ File committed: {filename}")
            else:
                print(f"✗ Failed to commit file")
    else:
        print("✗ Repository creation failed")

def task_star_trending(bot: 'ActivityBot') -> None:
    """Star random trending repository"""
    if not hasattr(task_star_trending, '_called_from_daily'):
        print("\n--- STAR TRENDING REPO ---")
    
    trending_repos = [
        "https://github.com/microsoft/vscode",
        "https://github.com/facebook/react",
        "https://github.com/tensorflow/tensorflow",
        "https://github.com/pytorch/pytorch",
        "https://github.com/golang/go",
        "https://github.com/rust-lang/rust",
        "https://github.com/kubernetes/kubernetes",
        "https://github.com/docker/docker-ce",
        "https://github.com/nodejs/node",
        "https://github.com/python/cpython"
    ]
    
    repo_url = random.choice(trending_repos)
    if not hasattr(task_star_trending, '_called_from_daily'):
        print(f"Target: {repo_url}")
    
    if bot.star_repository(repo_url):
        if not hasattr(task_star_trending, '_called_from_daily'):
            print("✓ Repository starred")
    else:
        if not hasattr(task_star_trending, '_called_from_daily'):
            print("✗ Star failed (might already starred)")

def task_follow_user(bot: 'ActivityBot') -> None:
    """Follow random popular user"""
    if not hasattr(task_follow_user, '_called_from_daily'):
        print("\n--- FOLLOW USER ---")
    
    popular_users = [
        "torvalds", "gvanrossum", "paulirish", "addyosmani",
        "sindresorhus", "tj", "defunkt", "pjhyett",
        "mojombo", "wycats", "dhh", "antirez"
    ]
    
    username = random.choice(popular_users)
    if not hasattr(task_follow_user, '_called_from_daily'):
        print(f"Target: {username}")
    
    if bot.follow_user(username):
        if not hasattr(task_follow_user, '_called_from_daily'):
            print(f"✓ Followed: {username}")
    else:
        if not hasattr(task_follow_user, '_called_from_daily'):
            print(f"✗ Follow failed (might already following)")

def task_browse_explore(bot: 'ActivityBot') -> None:
    """Browse & explore dengan pola human-like"""
    print("\n--- BROWSE & EXPLORE ---")
    
    activities = [
        ("Browse Trending", lambda: bot.browse_trending(duration_seconds=30)),
        ("Explore Python", lambda: bot.explore_topics("python", duration_seconds=20)),
        ("Explore JavaScript", lambda: bot.explore_topics("javascript", duration_seconds=20)),
        ("Explore Machine Learning", lambda: bot.explore_topics("machine-learning", duration_seconds=25)),
        ("Explore DevOps", lambda: bot.explore_topics("devops", duration_seconds=20))
    ]
    
    activity_name, activity_func = random.choice(activities)
    print(f"Activity: {activity_name}")
    
    try:
        activity_func()
        print(f"✓ {activity_name} completed")
    except Exception as e:
        print(f"✗ Error: {e}")

def task_commit_file(bot: 'ActivityBot') -> None:
    """Commit file ke existing repository"""
    print("\n--- COMMIT FILE ---")
    
    repo_name = input("Repository name: ").strip()
    if not repo_name:
        return
    
    # Generate file dari AI
    file_data = ai_core.generate_file_content(repo_name)
    if not file_data:
        print("✗ AI failed to generate file")
        return
    
    filename = file_data.get("filename")
    content = file_data.get("content")
    
    print(f"AI Generated File:")
    print(f"  Name: {filename}")
    print(f"  Size: {len(content)} chars")
    
    confirm = input("\nCommit file? (y/n): ").lower()
    if confirm != 'y':
        return
    
    commit_msg = input("Commit message (optional): ").strip() or f"Add {filename}"
    
    if bot.commit_file(repo_name, filename, content, commit_msg):
        print(f"✓ File committed: {filename}")
    else:
        print("✗ Commit failed")

def task_daily_activity(bot: 'ActivityBot') -> None:
    """Complete set of daily activities untuk avoid flag"""
    if not hasattr(task_daily_activity, '_called_from_multi'):
        print("\n" + "="*60)
        print("       DAILY ACTIVITY SET (Anti-Flag Protocol)")
        print("="*60)
        print("Akan menjalankan serangkaian aktivitas human-like:")
        print("  - Browse trending repositories")
        print("  - Explore 2-3 topics")
        print("  - Star 1-2 repos")
        print("  - Follow 1 user")
        print("  - Random delays between actions")
        print("="*60)
        
        confirm = input("\nMulai daily activity? (y/n): ").lower()
        if confirm != 'y':
            return
    
    try:
        # 1. Browse trending
        print("\n[1/5] Browsing trending...")
        bot.browse_trending(duration_seconds=random.randint(25, 40))
        time.sleep(random.uniform(5, 10))
        
        # 2. Explore topic 1
        print("\n[2/5] Exploring topic...")
        topics = ["python", "javascript", "docker", "kubernetes", "react"]
        bot.explore_topics(random.choice(topics), duration_seconds=random.randint(20, 30))
        time.sleep(random.uniform(5, 10))
        
        # 3. Star repo
        print("\n[3/5] Starring repository...")
        task_star_trending._called_from_daily = True
        task_star_trending(bot)
        delattr(task_star_trending, '_called_from_daily')
        time.sleep(random.uniform(5, 10))
        
        # 4. Explore topic 2
        print("\n[4/5] Exploring another topic...")
        bot.explore_topics(random.choice(topics), duration_seconds=random.randint(15, 25))
        time.sleep(random.uniform(5, 10))
        
        # 5. Follow user
        print("\n[5/5] Following user...")
        task_follow_user._called_from_daily = True
        task_follow_user(bot)
        if hasattr(task_follow_user, '_called_from_daily'):
            delattr(task_follow_user, '_called_from_daily')
        
        if not hasattr(task_daily_activity, '_called_from_multi'):
            print("\n" + "="*60)
            print("✓ DAILY ACTIVITY COMPLETED")
            print("="*60)
            print(f"Total runtime: ~{random.randint(3, 5)} minutes")
            print("Aktivitas ini membantu membangun pola behavior natural")
            print("="*60)
    
    except Exception as e:
        logging.error(f"Daily activity error: {e}")
        print(f"✗ Error during daily activity: {e}") "="*60)
    print("       DAILY ACTIVITY SET (Anti-Flag Protocol)")
    print("="*60)
    print("Akan menjalankan serangkaian aktivitas human-like:")
    print("  - Browse trending repositories")
    print("  - Explore 2-3 topics")
    print("  - Star 1-2 repos")
    print("  - Follow 1 user")
    print("  - Random delays between actions")
    print("="*60)
    
    confirm = input("\nMulai daily activity? (y/n): ").lower()
    if confirm != 'y':
        return
    
    try:
        # 1. Browse trending
        print("\n[1/5] Browsing trending...")
        bot.browse_trending(duration_seconds=random.randint(25, 40))
        time.sleep(random.uniform(5, 10))
        
        # 2. Explore topic 1
        print("\n[2/5] Exploring topic...")
        topics = ["python", "javascript", "docker", "kubernetes", "react"]
        bot.explore_topics(random.choice(topics), duration_seconds=random.randint(20, 30))
        time.sleep(random.uniform(5, 10))
        
        # 3. Star repo
        print("\n[3/5] Starring repository...")
        task_star_trending(bot)
        time.sleep(random.uniform(5, 10))
        
        # 4. Explore topic 2
        print("\n[4/5] Exploring another topic...")
        bot.explore_topics(random.choice(topics), duration_seconds=random.randint(15, 25))
        time.sleep(random.uniform(5, 10))
        
        # 5. Follow user
        print("\n[5/5] Following user...")
        task_follow_user(bot)
        
        print("\n" + "="*60)
        print("✓ DAILY ACTIVITY COMPLETED")
        print("="*60)
        print(f"Total runtime: ~{random.randint(3, 5)} minutes")
        print("Aktivitas ini membantu membangun pola behavior natural")
        print("="*60)
    
    except Exception as e:
        logging.error(f"Daily activity error: {e}")
        print(f"✗ Error during daily activity: {e}")

def task_marathon_mode(bot: 'ActivityBot') -> None:
    """1 jam aktivitas random untuk deep human simulation"""
    print("\n" + "="*60)
    print("          MARATHON MODE (1 Hour Session)")
    print("="*60)
    print("Bot akan menjalankan aktivitas random selama 1 jam:")
    print("  - Random browsing & exploring")
    print("  - Occasional starring & following")
    print("  - Natural delays & pauses")
    print("  - Simulates extended human session")
    print("="*60)
    
    confirm = input("\nMulai marathon mode? (y/n): ").lower()
    if confirm != 'y':
        return
    
    start_time = time.time()
    duration = 3600  # 1 hour
    action_count = 0
    
    activities = [
        ("browse_trending", lambda: bot.browse_trending(random.randint(30, 60))),
        ("explore_python", lambda: bot.explore_topics("python", random.randint(20, 40))),
        ("explore_javascript", lambda: bot.explore_topics("javascript", random.randint(20, 40))),
        ("explore_docker", lambda: bot.explore_topics("docker", random.randint(15, 30))),
        ("explore_ml", lambda: bot.explore_topics("machine-learning", random.randint(20, 35))),
        ("star_repo", task_star_trending),
        ("follow_user", task_follow_user)
    ]
    
    try:
        print(f"\n>>> Marathon started at {time.strftime('%H:%M:%S')}")
        
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            
            print(f"\n[{elapsed//60}m {elapsed%60}s / 60m] Action #{action_count + 1}")
            
            # Pick random activity
            activity_name, activity_func = random.choice(activities)
            print(f"Performing: {activity_name}")
            
            try:
                if activity_name in ["star_repo", "follow_user"]:
                    activity_func(bot)
                else:
                    activity_func()
                
                action_count += 1
                print(f"✓ Completed")
            
            except Exception as e:
                logging.error(f"Activity error: {e}")
                print(f"✗ Error: {e}")
            
            # Random delay between actions (2-10 minutes)
            if remaining > 120:  # If more than 2 min remaining
                delay = random.randint(120, 600)
                print(f"Idle for {delay//60}m {delay%60}s...")
                time.sleep(delay)
        
        print("\n" + "="*60)
        print("✓ MARATHON MODE COMPLETED")
        print("="*60)
        print(f"Total actions performed: {action_count}")
        print(f"Total runtime: 60 minutes")
        print("="*60)
    
    except KeyboardInterrupt:
        print(f"\n>>> Marathon interrupted after {int(time.time() - start_time)//60} minutes")
        print(f"Actions completed: {action_count}")
    except Exception as e:
        logging.error(f"Marathon error: {e}")
        print(f"✗ Marathon error: {e}")