import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timedelta, timezone


def extract_article(url):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract publication date
        date_tag = (
            soup.find("meta", {"property": "article:published_time"})
            or soup.find("meta", {"name": "article:published_time"})
            or soup.find("time")
        )

        published_date = None

        if date_tag:
            published_date = (
                date_tag.get("content")
                or date_tag.get("datetime")
                or date_tag.get_text(strip=True)
            )

        # Extract article text
        paragraphs = soup.find_all("p")

        text = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
            if len(p.get_text(strip=True)) > 40
        )

        return {
            "url": url,
            "published_date": published_date,
            "text": text
        }

    except Exception as e:
        print(f"Article extraction failed: {e}")
        return None


def is_last_24_hours(date_string):

    if not date_string:
        return False

    try:
        published = datetime.fromisoformat(
            date_string.replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        return now - timedelta(hours=24) <= published <= now

    except Exception:
        return False


if __name__ == "__main__":

    test_urls = [
        "https://techcrunch.com/2026/09/11/mecka-ai-nears-500m-valuation-in-sequoia-led-deal-amid-rush-for-robot-training-data/",
        "https://techcrunch.com/2026/09/11/kimi-maker-moonshot-ai-targets-2-billion-in-annual-revenue/"
    ]

    for url in test_urls:

        print("\nProcessing:")
        print(url)

        article = extract_article(url)

        if article:

            print("\nPublished:", article["published_date"])

            if is_last_24_hours(article["published_date"]):
                print("STATUS: Last 24 hours")
                print("Text length:", len(article["text"]))
                print("Preview:", article["text"][:300])
            else:
                print("STATUS: Older than 24 hours")