# Mini Flask URL Shortener

A simple URL shortener web app built with **Flask**.  
Shorten long URLs into easy-to-share short links and track click counts. This project is perfect for beginners to learn Flask, routing, forms, and JSON-based data storage.

---

## Features

- Shorten any long URL to a short, unique code.
- Option to create a **custom alias** for the short URL.
- Click on a short link to redirect to the original URL.
- View all shortened URLs and their click counts.
- Persistent storage using `urls.json`.
- JSON API endpoint to get all links: `/api/links`.

---

## Demo Screenshot

![Screenshot](./screenshot.png) <!-- Optional: Add a screenshot of your app here -->

---

## Prerequisites

- Python 3.8+ installed
- pip (Python package manager)

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener

# Create and activate a virtual environment:
# Windows
python -m venv env
env\Scripts\activate

# macOS / Linux
python -m venv env
source env/bin/activate

# Install dependencies:
pip install flask

# Usage

Run the app:

python app.py


Open your browser and go to:

http://127.0.0.1:5000/


Shorten URLs by entering a long URL and optionally a custom alias.

Visit /list to see all shortened URLs and click counts.

Access API endpoint:

http://127.0.0.1:5000/api/links

# Project Structure
url_shortener/
├─ app.py           # Main Flask app
├─ urls.json        # Stores URL mappings
├─ templates/       # HTML templates
│   ├─ layout.html
│   ├─ index.html
│   └─ list.html
└─ static/          # Static files (CSS, images)
    └─ style.css

# How It Works

User submits a long URL.

App generates a unique code or uses the custom alias.

Data is stored in urls.json:

{
  "abc123": { "url": "https://example.com", "clicks": 0 }
}


Redirects increment the clicks counter.

Users can view all links and click statistics.
