
# GitHub README Fetcher

A simple web application that fetches and displays the README file from a specified GitHub repository based on a username specified in a `config.json` file. The application uses Flask to serve the web page and provides an asynchronous loading experience for better user interaction.

## Features

- Automatically fetches the README file from a GitHub repository.
- Displays the content in a user-friendly format.
- Asynchronous loading to prevent waiting times on page load.
- Simple configuration via a JSON file.

## Prerequisites

- Python 3.6 or higher
- Flask
- `requests` library

## Installation

1. **Clone the repository** (or download the project files):

   ```bash
   git clone https://github.com/glitchmill/guitarr.git
   cd guitarr
   ```

2. **Install the required packages**:

   ```bash
   pip install Flask requests
   ```

3. **Create a `config.json` file** in the project directory with the following structure:

   ```json
   {
       "username": "your-github-username"
   }
   ```

   Replace `"your-github-username"` with the actual username of the GitHub repository you want to fetch the README from.

## Project Structure

```
/your-project-directory
│
├── fetch_readme.py       # The main Python application
├── config.json           # Configuration file for GitHub username
└── templates
    └── index.html        # HTML template for displaying README content
```

## Usage

1. **Run the application**:

   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:

   ```
   http://127.0.0.1:5000
   ```

3. The application will automatically fetch and display the README content from the specified GitHub repository.

## Troubleshooting

- If you encounter any errors fetching the README, ensure that the specified username in `config.json` is correct and that the repository exists.
- Ensure that you have a stable internet connection.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - A micro web framework for Python.
- [Requests](https://requests.readthedocs.io/en/latest/) - A simple HTTP library for Python.
