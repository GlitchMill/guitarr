
# Guitarr
  <!-- Update with your logo image link -->
## Overview

Guitarr is a web application that provides insights into your GitHub contributions and repositories. It fetches your recent contributions, displays your avatar, and showcases the README files from your repositories, all in a user-friendly interface.

## Features

- **User Contributions:** View your latest GitHub activity including pushes, pull requests, issues, and more.
- **Profile Information:** Displays your GitHub avatar and username.
- **Repository README:** Fetches and displays the README file from your repositories.
- **Timezone Support:** Time of contributions is displayed in your configured timezone.

## Installation

To set up the Guitarr application on your local machine, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/glitchmill/guitarr.git
   cd guitarr
   ```

2. **Install dependencies:**

   Make sure you have Python installed. You can install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your configuration:**

   Create a `config.json` file in the root directory with the following structure:

   ```json
   {
       "username": "your_github_username",
       "timezone": "your_timezone"  // e.g., "UTC", "America/New_York"
   }
   ```

4. **Run the application:**

   Start the Flask application:

   ```bash
   python app.py
   ```

5. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

- Upon loading the application, you will see your GitHub avatar and a list of your recent contributions.
- The README of your repository will be displayed below your contribution details.

## Contributing

Contributions are welcome! If you would like to contribute to Guitarr, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to [Flask](https://flask.palletsprojects.com/) for the web framework.
- Special thanks to [GitHub](https://github.com) for providing the API used in this application.

## Contact

For questions or inquiries, please reach out via GitHub.
