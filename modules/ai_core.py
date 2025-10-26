# modules/ai_core.py - AI Integration for Activity Bot

import os
import logging
import json
import random
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY tidak ditemukan di .env")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    logging.info("✓ Gemini AI connected")
except Exception as e:
    logging.critical(f"✗ Gemini AI failed: {e}")
    model = None

def generate_repo_name() -> dict:
    """Generate realistic repository name & description"""
    if not model:
        # Fallback jika AI tidak tersedia
        categories = ["utils", "toolkit", "helper", "manager", "analyzer"]
        tech = ["python", "js", "data", "web", "api"]
        name = f"{random.choice(tech)}-{random.choice(categories)}-{random.randint(100, 999)}"
        return {
            "repo_name": name,
            "description": f"A simple {random.choice(categories)} for {random.choice(tech)} projects"
        }
    
    prompt = """
    Generate a realistic GitHub repository name and description.
    The repo should look like a personal project or utility tool.
    
    Return ONLY valid JSON:
    {
      "repo_name": "short-lowercase-name",
      "description": "Brief description (max 80 chars)"
    }
    
    Examples:
    - data-cleaner-toolkit
    - python-api-wrapper
    - web-scraper-utils
    
    Make it creative but realistic.
    """
    
    try:
        response = model.generate_content(prompt)
        cleaned = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned)
        
        if "repo_name" in data and "description" in data:
            logging.info(f"AI generated repo: {data['repo_name']}")
            return data
        
        return None
    except Exception as e:
        logging.error(f"AI repo generation failed: {e}")
        return None

def generate_file_content(repo_name: str) -> dict:
    """Generate realistic file content"""
    if not model:
        # Fallback content
        file_types = [
            ("README.md", "# {}\n\nA simple project for learning purposes.\n\n## Features\n- Feature 1\n- Feature 2"),
            ("config.py", "# Configuration\nDEBUG = True\nVERSION = '1.0.0'\n"),
            (".gitignore", "*.pyc\n__pycache__/\n.env\nnode_modules/\n")
        ]
        filename, template = random.choice(file_types)
        return {
            "filename": filename,
            "content": template.format(repo_name)
        }
    
    prompt = f"""
    Generate a realistic file for a GitHub repository named '{repo_name}'.
    
    Choose ONE file type randomly:
    - Python script (.py)
    - JavaScript file (.js)
    - Markdown documentation (.md)
    - Configuration file (.json, .yaml, or .gitignore)
    
    Return ONLY valid JSON:
    {{
      "filename": "appropriate_name.ext",
      "content": "file content here (use \\n for newlines, max 50 lines)"
    }}
    
    Make the content realistic and functional.
    """
    
    try:
        response = model.generate_content(prompt)
        cleaned = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned)
        
        if "filename" in data and "content" in data:
            logging.info(f"AI generated file: {data['filename']}")
            return data
        
        return None
    except Exception as e:
        logging.error(f"AI file generation failed: {e}")
        return None

def get_next_activity(history: list) -> str:
    """AI decides next activity based on history"""
    if not model:
        # Fallback: random selection
        activities = ["browse_trending", "explore_topic", "star_repo", "follow_user"]
        return random.choice(activities)
    
    history_str = ", ".join(history[-10:]) if history else "None"
    
    prompt = f"""
    You are a GitHub activity scheduler. Goal: simulate natural human behavior.
    
    Recent activity history: [{history_str}]
    
    Available activities:
    - browse_trending
    - explore_topic
    - star_repo
    - follow_user
    - create_repo
    
    Based on history, what's the most natural next activity?
    Return ONLY the activity name (one word).
    
    Rules:
    - Avoid repeating same activity consecutively
    - Balance between passive (browsing) and active (starring) actions
    - If history is empty, start with browse_trending
    """
    
    try:
        response = model.generate_content(prompt)
        activity = response.text.strip().lower().replace('"', '').replace("'", "")
        
        valid_activities = ["browse_trending", "explore_topic", "star_repo", "follow_user", "create_repo"]
        
        if activity in valid_activities:
            logging.info(f"AI suggests: {activity}")
            return activity
        
        return "browse_trending"
    except Exception as e:
        logging.error(f"AI activity selection failed: {e}")
        return "browse_trending"