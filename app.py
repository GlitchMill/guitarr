from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Load the username from config.json
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# Fetch the README file from the GitHub repository
def fetch_readme(username):
    url = f"https://raw.githubusercontent.com/{username}/{username}/refs/heads/main/README.md"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        return "Error: The request timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route('/')
def index():
    config = load_config()
    username = config.get("username")
    return render_template('index.html', username=username)

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
