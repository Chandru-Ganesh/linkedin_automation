# LinkedIn Automation Bot

This project is a LinkedIn automation tool that helps you log in to LinkedIn, search for people (even 2nd or 3rd degree connections), and scrape their full profile information using Playwright.

The main goal is to collect only the actual profile content (not sidebar recommendations) and export everything into a clean text file.

---

## 💡 Features

- Log in using LinkedIn session or API
- Search and visit specific user profiles
- Automatically open a person's LinkedIn page
- Scrape main profile details using Playwright
- Save output into a `.txt` file

---

## 🚀 How to Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/linkedin-automation-bot.git
   cd linkedin-automation-bot
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
playwright install
Update the target profile URL in the script

Run the bot

bash
Copy
Edit
python linkedin_scraper.py
Check the output

The scraped profile content will be saved as a .txt file in the project directory.

## 📌 Note
This project is for educational and research purposes only.

Avoid overusing automation on LinkedIn to prevent account restrictions.

🔄 Coming Soon
Auto-connection requests

Message automation

Structured output in CSV or JSON format
