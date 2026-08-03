# 📰 UAF News Web Scraper

A high-performance Python web scraper built with **Playwright** and **BeautifulSoup4** to extract the latest official news announcements, headlines, timestamps, event locations, and detail links from the **University of Agriculture, Faisalabad (UAF)** news portal.

---

## 🚀 Key Features

* **Dual-Phase Extraction Strategy:** Scrapes listing card metadata (time, location, date) from the catalog page and seamlessly resolves full, non-truncated headlines from individual article pages.
* **Defensive Scraping Architecture:** Features conditional element inspection and fallback chains to prevent crashes on missing HTML attributes or inconsistent DOM structures.
* **Structured CLI Presentation:** Formats multi-line headlines and metadata using Python's native `textwrap` module for a clean, readable terminal user interface.
* **Headless Browser Execution:** Utilizes Playwright Chromium in headless mode for fast, modern web rendering.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.8+
* **Browser Automation:** [Playwright](https://playwright.dev/python/)
* **HTML Parsing:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* **Parser Engine:** `lxml`
* **Formatting:** `textwrap`, `urllib.parse`

---

## ⚙️ Installation & Setup

1. **Clone or navigate to the repository directory:**
   ```bash
   cd python-projects/uaf-news-scraper