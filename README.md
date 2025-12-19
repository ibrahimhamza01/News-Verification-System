# Fake News Detection System

## Overview
This project detects and verifies the authenticity of news articles by analyzing content and comparing it across trusted sources.  
It combines **React** for the frontend, **Django** for the backend, **NLP embeddings (SentenceTransformer)** for text similarity, and **Selenium** for automated web scraping.

The system helps users identify fake news by comparing news content with multiple trusted sources and computing similarity scores.


## Features
- Analyze and verify news content automatically  
- Compare news with trusted sources using NLP embeddings  
- Web scraping using Selenium for real-time source checking  
- Backend built in Django, frontend in React  
- Quick detection of suspicious or misleading news  


## Project Structure

News-Verification-System/
├── comparisons/ # Django app for comparison logic
│ ├── migrations/
│ ├── pycache/
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── nlp_proj/ # Django project folder
│ ├── pycache/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── db.sqlite3 # SQLite database (optional)
└── manage.py # Django management script



## Requirements

- Python 3.x  
- Django  
- React (frontend)  
- SentenceTransformer (`pip install sentence-transformers`)  
- Selenium (`pip install selenium`)  
- ChromeDriver or other browser driver for Selenium  


## Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/NewsVerificationSystem.git
cd NewsVerificationSystem
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
```

3. Run Django server

```bash
python manage.py runserver
```

4. Start the frontend (React app)

```bash
cd frontend
npm install
npm start
```

5. Use the system

Enter news content in the frontend input form

The system will scrape trusted sources, compute similarity scores, and output a verification result

## Notes

Ensure Selenium is configured with the correct browser driver (ChromeDriver/GeckoDriver)

This system focuses on text verification only, not images or videos

Database (db.sqlite3) stores intermediate results and scraped content
