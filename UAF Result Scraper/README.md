# 📰 UAF Result Scraper

A Python-based automation tool that extracts student results directly from the **University of Agriculture, Faisalabad (UAF)** LMS portal. It bypasses the manual login process for result checking and presents the data in a clean, formatted command-line interface.

## 🚀 Features
*   **Headless Automation**: Uses Playwright to navigate the LMS portal in the background without opening a visible browser window.
*   **Formatted Output**: Parses raw HTML tables into a readable, structured block showing Course IDs, Total Marks, and Grades.
*   **Error Handling**: Includes robust handling for server timeouts, network issues, and invalid AG number formats.
*   **Cross-Platform**: Works on Windows, macOS, and Linux.

## 📋 Prerequisites
*   **Python 3.8+** installed on your system.
*   **pip** (Python package manager).

## 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com
    cd uaf-result-scraper
    ```

2.  **Create a Virtual Environment (Recommended)**
    *   **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browsers**
    This script requires the Chromium browser engine.
    ```bash
    playwright install chromium
    ```

## 💻 Usage

1.  **Run the Script**
    ```bash
    python main.py
    ```
    *(Note: Replace `main.py` with whatever you named your script file)*

2.  **Enter Credentials**
    When prompted, enter your Registration Number in the standard format:
    ```text
    Enter your AG Number (****-ag-****): 2022-ag-1234
    ```

3.  **View Results**
    The script will fetch the data and display it in the terminal:
    ```text
    ==================================================
    2022-ag-1234      STUDENT NAME
    Degree:           B.Sc (Hons.) Agri. Sciences
    ==================================================
    Course    Total     Grade     Status
    --------------------------------------------------
    CS-101    60        A         PASS      
    AGRON-301 80        B+        PASS      
    ==================================================
    ```

## ⚠️ Disclaimer
This tool is for **educational purposes only**. It is designed to facilitate students in checking their own results efficiently. Please do not use this tool to spam the university servers or unauthorized data scraping.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com)
