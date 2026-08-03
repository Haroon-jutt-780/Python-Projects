# 📰 UAF News Web Scraper

A high-performance, interactive Python web scraper built with **Playwright** and **BeautifulSoup4** to extract the latest official news announcements, headlines, timestamps, event locations, and detail links from the **University of Agriculture, Faisalabad (UAF)** news portal.

---

## 🚀 Key Features

* **Interactive CLI Interface:** Dynamically prompts the user at runtime for the exact number of news articles to scrape, complete with input validation and error handling.
* **Smart Latency Reduction:** Initiates initial page loading in the background while waiting for user input to speed up execution.
* **Guaranteed Resource Cleanup:** Engineered with `try...finally` blocks to guarantee Chromium browser processes close cleanly without memory leaks—even if canceled with `Ctrl + C`.
* **Dual-Phase Extraction Strategy:** Scrapes listing card metadata (time, location) from the main catalog page and seamlessly combines it with full, non-truncated headlines and dates from individual detail pages.
* **Structured UI Presentation:** Automatically manages terminal screens and formats multi-line headlines using Python's native `textwrap` module for a polished CLI interface.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.8+
* **Browser Automation:** [Playwright](https://playwright.dev/python/)
* **HTML Parsing:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* **Parser Engine:** `lxml`
* **Formatting & Utilities:** `textwrap`, `os`

---

## ⚙️ Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd "UAF Latest News Scraper"
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