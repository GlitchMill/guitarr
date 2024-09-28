from flask import Flask, render_template, request
import requests
import json
import time

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

# Fetch contributions from GitHub
def fetch_contributions(username):
    url = f"https://api.github.com/users/{username}/events/public"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        events = response.json()
        contributions = []
        for event in events[:5]:  # Get the last 5 events
            contributions.append({
                'type': event['type'],
                'repo': event['repo']['name'],
                'created_at': event['created_at'],
                'payload': event.get('payload', {})
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
