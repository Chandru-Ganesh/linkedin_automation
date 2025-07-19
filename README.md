# 🤖 LinkedIn Automation Bot (Python)

This is a **Python-based LinkedIn automation tool** that:

✅ Logs into your LinkedIn account using your credentials  
✅ Navigates to a **target LinkedIn profile URL**  
✅ Sends a **connection request with a custom message (note)**  
✅ If already connected, sends a **direct message**  
✅ If no connect option exists, optionally follows the user  
✅ Persists session during runtime  
✅ Uses smart waiting strategies to avoid bot detection

---

## 🛠 Features

- 🔐 Secure login via LinkedIn username/password
- 🔗 Profile visit by URL
- 🤝 Connection requests with optional note (up to 300 chars)
- 💬 Message target user if already connected
- 📡 Automatically detects connection status
- 🧠 Handles layout/UI variations (Connect inside dropdowns, etc.)
- 👤 Stealth-mode: uses undetected-chromedriver for anti-bot detection
- 🚀 Fully modular and extensible
- 🧹 Gracefully closes session after execution

---

## 📂 Project Structure

linkedin_automation/
├── requirements.txt
└── app/
├── main.py # Entry point (FastAPI app)
├── routers/
│ └── linkedin.py # API endpoint logic
├── services/
│ └── linkedin_bot.py # LinkedIn bot automation logic
├── sessions/
│ └── session_manager.py # Manages session state
└── utils/
└── wait_utils.py # Smart waiting functions


---

## 🧪 Prerequisites

- Python 3.9+
- Google Chrome installed
- ChromeDriver auto-installed by `undetected-chromedriver`

---

## 📦 Installation

1. **Clone the repository**

git clone https://github.com/your-username/linkedin_automation.git
cd linkedin_automation


2. **Create a virtual environment (optional but recommended)**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Run the FastAPI server**
uvicorn app.main:app --reload

## 🔐 Environment Setup
Create a .env file (or pass directly in JSON payload):

LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_secure_password
📬 API Endpoints (FastAPI)

## ✅ 1. POST /login
Logs in to LinkedIn and stores browser session.

Request body:

{
  "username": "your_email@example.com",
  "password": "your_password"
}

## ✅ 2. POST /connect
Navigates to a profile and sends a connection request with custom message.

Request body:


{
  "profile_url": "https://www.linkedin.com/in/target-user/",
  "message": "Hi! I'd love to connect with you professionally."
}

## ✅ 3. POST /check_connection
If the profile is already connected, sends the given message.

Request body:

json
Copy
Edit
{
  "profile_url": "https://www.linkedin.com/in/target-user/",
  "message": "Thanks for connecting! Excited to collaborate."
}

## ✅ 4. GET /close
Gracefully closes the browser session.

## 🛡 Anti-Detection Techniques
- Uses undetected-chromedriver for stealth browsing

- Smart element waits (no hardcoded timeouts)

- Resilient selectors for dynamic LinkedIn UI

- Optional headless mode

## ⚠️ Limitations
This tool mimics real browser behavior but cannot bypass LinkedIn limits

CAPTCHA is not handled (you will be prompted manually if triggered)

Use at your own risk — excessive automation may violate LinkedIn’s Terms

## 👨‍💻 Developer Notes
✅ Built using Python 3, FastAPI, Selenium, undetected-chromedriver

🧩 Easily extensible for bulk profiles, analytics, auto-replies, and more

🗂 Can be containerized with Docker (optional)

**✅ Example Run (Manual Script Mode)**
You can also test the core bot without API:

python app/services/linkedin_bot.py

## ✨ Future Improvements
 Add Docker support

 Add proxy/rotating user agents

 Support CSV for batch profile messaging

 Add GUI or web dashboard (optional)

## 🙏 Disclaimer
This bot is for educational and personal use only.
We are not affiliated with LinkedIn. Use this responsibly.

## 📧 Contact
Maintained by Chandru Ganesh
Feel free to star ⭐ the repo and submit issues or feature requests!


---

## Let me know if you want:
- Docker setup in this README
- Sample `.env` or `curl` testing commands
- Or a GUI wrapper using Tkinter or Flask

Ready to go 🚀

---
```bash
Note : This bot is under development, it was successfull for a point. but I get struck in single point, but not to worry i will upload the updates and makes it complete automation in upcoming days.

THANK YOU
