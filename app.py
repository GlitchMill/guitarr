from flask import Flask, render_template, request
import requests
import json
import time
from datetime import datetime
import pytz

app = Flask(__name__)

# Load the username from config.json
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# Cache for storing README content
readme_cache = {}
CACHE_TIMEOUT = 3600  # Cache timeout in seconds (1 hour)

# Fetch the README file from the GitHub repository
def fetch_readme(username):
    if username in readme_cache and (time.time() - readme_cache[username]['timestamp']) < CACHE_TIMEOUT:
        return readme_cache[username]['content']
    
    url = f"https://raw.githubusercontent.com/{username}/{username}/refs/heads/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        readme_content = response.text
        readme_cache[username] = {'content': readme_content, 'timestamp': time.time()}
        return readme_content
    except requests.exceptions.Timeout:
        return "Error: The request timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Fetch the user's avatar URL from GitHub
def fetch_avatar(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        user_data = response.json()
        return user_data.get('avatar_url', 'default_avatar.png')
    except requests.exceptions.RequestException:
        return 'default_avatar.png'

# Mapping of GitHub event types to friendly names
EVENT_TYPE_MAP = {
    "PushEvent": "Pushed code to",
    "PullRequestEvent": "Created a pull request in",
    "IssuesEvent": "Opened an issue in",
    "ForkEvent": "Forked the repository",
    "CreateEvent": "Created a new repository",
    # Add more mappings as needed
}

def fetch_contributions(username):
    config = load_config()
    user_timezone = config.get("timezone", "UTC")
    url = f"https://api.github.com/users/{username}/events/public"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        events = response.json()
        contributions = []
        for event in events[:5]:  # Get the last 5 events
            # Convert the timestamp to the user's timezone
            event_time_utc = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            event_time_utc = event_time_utc.replace(tzinfo=pytz.utc)
            user_tz = pytz.timezone(user_timezone)
            event_time_local = event_time_utc.astimezone(user_tz)
            
            # Format the time in 24-hour and DD/MM/YYYY format
            friendly_time = event_time_local.strftime('%H:%M %d/%m/%Y')

            # Get the user-friendly event type
            event_type = EVENT_TYPE_MAP.get(event['type'], event['type'])
            
            # Append the repo name and URL for linking
            repo_name = event['repo']['name']
            repo_url = f"https://github.com/{repo_name}"
            
            # Build the readable contribution message
            contributions.append({
                'description': f"{event_type} {repo_name}",
                'repo': repo_name,
                'repo_url': repo_url,
                'created_at': friendly_time
            })
        return contributions
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route('/')
def index():
    config = load_config()
    username = config.get("username")
    avatar_url = fetch_avatar(username)
    contributions = fetch_contributions(username)
    return render_template('index.html', username=username, avatar_url=avatar_url, contributions=contributions)

@app.route('/fetch_readme')
def fetch_readme_route():
    username = request.args.get("username")
    if username:
        readme_content = fetch_readme(username)
        return readme_content
    else:
        return "Error: Username not found."

if __name__ == "__main__":
    app.run(debug=True)
