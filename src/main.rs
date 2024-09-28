use reqwest::blocking::Client;
use scraper::{Html, Selector};
use std::fs::File;
use std::io::copy;
use std::path::Path;
use std::error::Error;

// Function to download the README.md file
fn download_readme(username: &str) -> Result<(), Box<dyn Error>> {
    let url = format!("https://raw.githubusercontent.com/{username}/{username}/refs/heads/main/README.md");
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
    let username = "glitchmill"; // Replace this with the desired GitHub username
    let profile_url = format!("https://github.com/{}/", username);

    // 1. Scrape the avatar URL
    let client = Client::new();
    let response = client.get(&profile_url).send()?.text()?;

    if let Some(avatar_url) = scrape_avatar_url(&response) {
        println!("Found avatar URL: {}", avatar_url);
    } else {
        println!("No avatar URL found on the page.");
    }

    // 2. Download the README.md file
    download_readme(username)?;

    Ok(())
}
