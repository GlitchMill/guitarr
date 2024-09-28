use std::fs::File;
use std::io::copy;
use std::path::Path;
use reqwest::blocking::Client;
use std::error::Error;

fn download_file(url: &str, output_path: &Path) -> Result<(), Box<dyn Error>> {
    let client = Client::new();
    let response = client.get(url).send()?;

    if response.status().is_success() {
        let mut file = File::create(output_path)?;
        let mut content = response.bytes()?;
        copy(&mut content.as_ref(), &mut file)?;
        println!("File downloaded to {:?}", output_path);
    } else {
        println!("Failed to download the file: {}", response.status());
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let username = "GlitchMill";
    let url = format!("https://raw.githubusercontent.com/{username}/{username}/refs/heads/main/README.md");
    let output_path = Path::new("README.md");

    download_file(&url, output_path)?;

    Ok(())
}
