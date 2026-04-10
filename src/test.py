import pandas as pd


from selenium import webdriver
from selenium.webdriver.common.by import By


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(options=options)

def parse_all(driver):
    all_rows = []
    dates = pd.date_range(start="2025-11-01", end="2026-04-08", freq="D")

    for current_date in dates:
        year_month = current_date.strftime("%Y-%m")
        day = current_date.strftime("%d")

        for page_num in range(1, 4):
            url = f"{BASE_URL}/sitemap/{year_month}/{day}/{page_num}/"
            print(url)

            driver.get(url)
            close_cookie_popup(driver)

            cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='FeedListItem']")

            if len(cards) == 0:
                break

            for card in cards:
                card_time_text = card.find_element(By.CSS_SELECTOR, "[data-testid='DateLineText']").text.strip()
                title = card.find_element(By.CSS_SELECTOR, "[data-testid='TitleHeading']").text.strip()
                description = card.find_element(By.CSS_SELECTOR, "[data-testid='Description']").text.strip()
                article_url = card.find_element(By.CSS_SELECTOR, "[data-testid='TitleLink']").get_attribute("href")

                if article_url.startswith(BASE_URL):
                    article_path = article_url.replace(BASE_URL, "")
                else:
                    article_path = article_url

                parts = article_path.strip("/").split("/")
                section = ""
                subsection = ""

                if len(parts) >= 2 and parts[0] == "article":
                    section = parts[1]
                if len(parts) >= 3 and parts[0] == "article":
                    subsection = parts[2]

                all_rows.append({
                    "archive_date": current_date.strftime("%Y-%m-%d"),
                    "archive_year": current_date.year,
                    "archive_month": current_date.month,
                    "archive_day": current_date.day,
                    "archive_page": page_num,
                    "card_time_text": card_time_text,
                    "title": title,
                    "description": description,
                    "article_url": article_url,
                    "article_path": article_path,
                    "section": section,
                    "subsection": subsection,
                    "source_page_url": url,
                })

    return all_rows


def main():
    driver = create_driver()

    rows = parse_all(driver)
    df = pd.DataFrame(rows)

    print(df.shape)
    print(df.head(10))

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    input("")
    driver.quit()