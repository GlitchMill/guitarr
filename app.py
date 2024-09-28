from flask import Flask, render_template, request
import requests
import json
import time
from datetime import datetime
import pytz
import markdown

app = Flask(__name__)

# Load the username from config.json
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# Cache for storing README content
readme_cache = {}
CACHE_TIMEOUT = 3600  # Cache timeout in seconds (1 hour)

def fetch_user_languages(username):
    repos_url = f"https://api.github.com/users/{username}/repos"
    
    try:
        repos_response = requests.get(repos_url, timeout=10)
        repos_response.raise_for_status()
        repos_data = repos_response.json()
        
        language_count = {}
        for repo in repos_data:
            # Skip private and archived repositories
            if repo.get('private') or repo.get('archived'):
                continue
            
            # Get the languages used in the repository
            languages_url = repo.get('languages_url')
            languages_response = requests.get(languages_url, timeout=10)
            languages_response.raise_for_status()
            languages_data = languages_response.json()
            
            # Update language count (just keep the language names)
            for language in languages_data.keys():
                language_count[language] = language_count.get(language, 0) + 1  # Count occurrences

        # Sort languages by count of occurrences
        most_used_languages = sorted(language_count.items(), key=lambda x: x[1], reverse=True)
        return [lang for lang, _ in most_used_languages[:5]]  # Get the top 5 languages without bytes
    except requests.exceptions.RequestException:
        return []

def fetch_user_data(username):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"
    
    try:
        # Fetch user data
        user_response = requests.get(user_url, timeout=10)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Fetch repositories to get the stars count and open repos count
        repos_response = requests.get(repos_url, timeout=10)
        repos_response.raise_for_status()
        repos_data = repos_response.json()
        
        # Calculate total stars and open repositories
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        open_repos_count = sum(1 for repo in repos_data if not repo.get('private') and not repo.get('archived'))

        # Fetch most used languages
        most_used_languages = fetch_user_languages(username)

        return {
            'avatar_url': user_data.get('avatar_url', 'default_avatar.png'),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'stars': total_stars,
            'open_repos': open_repos_count,  
            'most_used_languages': most_used_languages
        }
    except requests.exceptions.RequestException:
        return {
            'avatar_url': 'default_avatar.png',
            'followers': 0,
            'following': 0,
            'stars': 0,
            'open_repos': 0,  
            'most_used_languages': []  
        }


def fetch_readme(username):
    if username in readme_cache and (time.time() - readme_cache[username]['timestamp']) < CACHE_TIMEOUT:
        return readme_cache[username]['content']
    
    # Try to fetch from the 'main' branch first
    url_main = f"https://raw.githubusercontent.com/{username}/{username}/refs/heads/main/README.md"
    url_master = f"https://raw.githubusercontent.com/{username}/{username}/refs/heads/master/README.md"
    
    try:
        # Attempt to fetch README from the main branch
        response = requests.get(url_main, timeout=10)
        response.raise_for_status()
        readme_content = response.text
    except requests.exceptions.HTTPError as e:
        # If fetching from main fails, try fetching from the master branch
        if response.status_code == 404:
            try:
                response = requests.get(url_master, timeout=10)
                response.raise_for_status()
                readme_content = response.text
            except requests.exceptions.RequestException as e:
                return f"Error fetching from master branch: {e}"
        else:
            return f"Error fetching from main branch: {e}"
    except requests.exceptions.Timeout:
        return "Error: The request timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

    # Convert Markdown to HTML
    html_content = markdown.markdown(readme_content)

    # Cache the README content
    readme_cache[username] = {'content': html_content, 'timestamp': time.time()}
    return html_content


# Mapping of GitHub event types to friendly names
EVENT_TYPE_MAP = {
    "PushEvent": "Pushed code to",
    "PullRequestEvent": "Created a pull request in",
    "IssuesEvent": "Opened an issue in",
    "ForkEvent": "Forked the repository",
    "CreateEvent": "Created a new repository",
    "DeleteEvent": "Deleted a repository or branch",
    "WatchEvent": "Starred the repository",
    "ReleaseEvent": "Published a release in",
    "IssueCommentEvent": "Commented on an issue in",
    "PullRequestReviewEvent": "Reviewed a pull request in",
    "PullRequestReviewCommentEvent": "Commented on a pull request in",
    "CommitCommentEvent": "Commented on a commit in",
    "DeploymentEvent": "Deployed the repository",
    "DeploymentStatusEvent": "Changed the status of a deployment in",
    "RepositoryEvent": "Created or updated a repository",
    "MembershipEvent": "Added or removed a collaborator in",
    "ProjectEvent": "Modified a project in",
    "ProjectCardEvent": "Modified a card in a project",
    "ProjectColumnEvent": "Modified a column in a project",
    "GollumEvent": "Updated the wiki in",
    "PublicEvent": "Made the repository public",
    "StatusEvent": "Changed the status of a commit in",
    "WatchEvent": "Watched the repository",
    "LabelEvent": "Added or removed labels in",
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
    user_data = fetch_user_data(username)
    contributions = fetch_contributions(username)

    return render_template(
        'index.html', 
        username=username, 
        avatar_url=user_data['avatar_url'],
        followers=user_data['followers'],
        following=user_data['following'],
        stars=user_data['stars'],  # Include stars count
        open_repos=user_data['open_repos'],  # Include open repos count
        most_used_languages=user_data['most_used_languages'],  # Include most used languages
        contributions=contributions
    )




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
