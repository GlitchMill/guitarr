use reqwest::blocking::Client;
use scraper::{Html, Selector};
use serde::Deserialize;
use std::fs::File;
use std::io::{self, BufReader, copy};
use std::path::Path;
use std::error::Error;

// Struct to represent the data in config.json
#[derive(Deserialize)]
struct Config {
    github_username: String,
}

// Function to read and parse config.json
fn read_config() -> Result<Config, Box<dyn Error>> {
    let file = File::open("config.json")?;
    let reader = BufReader::new(file);
    let config: Config = serde_json::from_reader(reader)?;
    Ok(config)
}

// Function to download the README.md file
fn download_readme(username: &str) -> Result<(), Box<dyn Error>> {
    let url = format!("https://raw.githubusercontent.com/{username}/{username}/refs/heads/main/README.md", );
    let output_path = Path::new("README.md");

    let client = Client::new();
    let response = client.get(&url).send()?;

    if response.status().is_success() {
        let mut file = File::create(output_path)?;
        let content = response.bytes()?;
        copy(&mut content.as_ref(), &mut file)?;
        println!("README.md downloaded to {:?}", output_path);
    } else {
        println!("Failed to download README.md: {}", response.status());
    }

    Ok(())
}

// Function to scrape the avatar URL from a GitHub page
fn scrape_avatar_url(html: &str) -> Option<String> {
    let document = Html::parse_document(html);
    let selector = Selector::parse("img").unwrap();

    for element in document.select(&selector) {
        if let Some(src) = element.value().attr("src") {
            if src.contains("https://avatars.githubusercontent.com/") {
                // Strip anything after the '?' in the URL
                let clean_url = src.split('?').next().unwrap_or(src).to_string();
                return Some(clean_url);
            }
        }
    }

    None
}

fn main() -> Result<(), Box<dyn Error>> {
    // 1. Read the GitHub username from config.json
    let config = read_config()?;
    let username = config.github_username;
    let profile_url = format!("https://github.com/{}/", username);

    // 2. Scrape the avatar URL
    let client = Client::new();
    let response = client.get(&profile_url).send()?.text()?;

    if let Some(avatar_url) = scrape_avatar_url(&response) {
        println!("Found avatar URL: {}", avatar_url);
    } else {
        println!("No avatar URL found on the page.");
    }

    // 3. Download the README.md file
    download_readme(&username)?;

    Ok(())
}
