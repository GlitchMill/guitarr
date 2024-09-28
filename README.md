
# Guitarr

Guitarr is a simple Rust-based command-line tool that performs the following tasks:
1. Scrapes a GitHub profile page to extract the avatar URL.
2. Downloads the `README.md` file from the GitHub repository matching the provided username.

## Features

- **GitHub Avatar Scraper**: Extracts and prints the avatar URL from the specified user's GitHub profile.
- **README.md Downloader**: Downloads the `README.md` file from the GitHub repository that shares the same name as the user.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/glitchmill/guitarr.git
   cd guitarr
   ```

2. Build the project using Cargo:
   ```bash
   cargo build --release
   ```

## Configuration

Create a `config.json` file in the root directory with the following structure:
```json
{
  "github_username": "your-github-username"
}
```

This configuration file provides the GitHub username required to scrape the profile and download the corresponding `README.md`.

## Usage

To run the application:

```bash
cargo run --release
```

The application will:
1. Scrape the GitHub page for the avatar URL and print it to the console.
2. Download the `README.md` file from the user's GitHub repository.

## Dependencies

- [Reqwest](https://crates.io/crates/reqwest): For making HTTP requests.
