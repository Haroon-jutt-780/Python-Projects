import textwrap
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()


    page.goto("https://web.uaf.edu.pk/News/AllNews")
    html_data = page.content()
    soup = BeautifulSoup(html_data, "lxml")

    #creating cards to get the url, time and location of each card
    cards = soup.select('.course-item')
    new_items = []

    for card in cards[:3]:
        #Extracting URLs
        a_tag = card.select_one('a[href*="NewsDetail"]')
        relative_path = a_tag['href'] if a_tag else ""
        full_url = f"https://web.uaf.edu.pk{relative_path}"

        #Extracting Times
        clock_icon = card.select_one('i.fa-clock')
        time_text = clock_icon.parent.get_text(strip=True) if clock_icon else "N/A"

        #Extracting Locations
        map_icon = card.select_one("i.fa-map-marker-alt")
        location_text = map_icon.parent.get_text(strip=True) if map_icon else "N/A"

        new_items.append({
            "url": full_url,
            "time": time_text,
            "location": location_text,
            })


    for index, item in enumerate(new_items):

        #Extract each URL
        page.goto(item["url"])
        html_data = page.content()
        soup = BeautifulSoup(html_data, "lxml")

        #Extract each Headline
        headline_el = soup.find("h5", class_="mb-3")
        headline = headline_el.get_text(strip=True) if headline_el else "N/A"

        #Extracting each Date
        li_tag = soup.find('li', class_='mr-3')
        date_text = "N/A"

        if li_tag and li_tag.find('a'):
            date_text = li_tag.find('a').get_text(strip=True).replace("Date:", "").strip()

        #Format long headline cleanly
        wrapped_headline = textwrap.fill(
            headline, 
            width=75, 
            initial_indent="📌 Headline: ", 
            subsequent_indent="            "
        )

        #Print clean formatted block
        print("=" * 70)
        print(f"   📰 NEWS ARTICLE #{index + 1}")
        print("=" * 70)
        print(wrapped_headline)
        print(f"📅 Date:     {date_text}")
        print(f"⏰ Time:     {item['time']}")
        print(f"📍 Location: {item['location']}")
        print(f"🔗 Link:     {item['url']}")
        print("-" * 70 + "\n")


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
