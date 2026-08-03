# 📰 UAF News Web Scraper

A high-performance, robust Python web scraper built with **Playwright** and **BeautifulSoup4** to extract the latest official news announcements, headlines, timestamps, event locations, and detail links from the **University of Agriculture, Faisalabad (UAF)** news portal.

---

## 🚀 Key Features

* **Configurable Scraping Limit:** Easily adjust the `MAX_NEWS_ITEMS` constant at the top of the script to scrape any desired number of news articles.
* **Dual-Phase Extraction Strategy:** Scrapes listing card metadata (time, location) from the main catalog page and seamlessly combines it with full, non-truncated headlines and dates from individual detail pages.
* **Defensive Scraping Architecture:** Features element existence checks, fallback selector chains, and dynamic URL assembly using `urljoin` to prevent crashes from missing DOM elements or broken links.
* **Structured CLI Presentation:** Formats multi-line headlines using Python's native `textwrap` module, complete with section dividers and emojis for a polished, readable terminal user interface.
* **Headless Automation:** Powered by Playwright Chromium running in headless mode for fast, modern JavaScript-enabled page rendering.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.8+
* **Browser Automation:** [Playwright](https://playwright.dev/python/)
* **HTML Parsing:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* **Parser Engine:** `lxml`
* **Formatting & Utilities:** `textwrap`, `urllib.parse`

---

## ⚙️ Configuration & Usage

### 1. Setting the News Limit
At the top of `main.py`, modify the `MAX_NEWS_ITEMS` constant to set how many articles you want to scrape:

```python
# --- CONFIGURATION CONSTANTS ---
MAX_NEWS_ITEMS = 3  # Change this to 5, 10, etc., to scrape more articles
```

### 2. Running the Scraper
Run the script directly from your active virtual environment terminal:

```bash
python main.py
```

---

## ⚙️ Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd "UAF Latest News Scraper"
   ```

2. **Activate your virtual environment:**
   ```powershell
   # On Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Chromium browser binaries:**
   ```bash
   playwright install chromium
   ```

---

## 💻 Sample Terminal Output

```text
======================================================================
   📰 NEWS ARTICLE #1
======================================================================
📌 Headline: One-day seminar on "Plant Breeders' Rights and Plant 
            Variety Protection" arranged by the Department of Plant 
            Breeding and Genetics, University of Agriculture Faisalabad.
📅 Date:     7/27/2026
⏰ Time:     10:12 AM
📍 Location: Seed Science
🔗 Link:     https://web.uaf.edu.pk/News/NewsDetail/2154
----------------------------------------------------------------------

======================================================================
   📰 NEWS ARTICLE #2
======================================================================
📌 Headline: A three-member Chinese delegation from the Institute of 
            Vegetable and Flowers (IVF), Chinese Academy of Agricultural 
            Sciences (CAAS) visited University of Agriculture Faisalabad.
📅 Date:     7/24/2026
⏰ Time:     11:34 AM
📍 Location: University of Agriculture
🔗 Link:     https://web.uaf.edu.pk/News/NewsDetail/2153
----------------------------------------------------------------------

======================================================================
   📰 NEWS ARTICLE #3
======================================================================
📌 Headline: Researchers called for innovation-led, inclusive and 
            resource-efficient agricultural development to address 
            climate change challenges.
📅 Date:     7/24/2026
⏰ Time:     10:36 AM
📍 Location: CAS Conference Room
🔗 Link:     https://web.uaf.edu.pk/News/NewsDetail/2152
----------------------------------------------------------------------
```

---

## 📝 License

Distributed under the **MIT License**.