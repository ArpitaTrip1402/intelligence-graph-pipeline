import requests
from bs4 import BeautifulSoup


def get_paper_info(paper_url):

    response = requests.get(paper_url)

    if response.status_code != 200:
        print("Failed to fetch paper")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1", class_="title").get_text(" ", strip=True)
    title = title.replace("Title:", "").strip()

    authors = soup.find("div", class_="authors").get_text(" ", strip=True)
    authors = authors.replace("Authors:", "").replace(":", "").strip()

    published = soup.find(
        "meta",
        {"name": "citation_date"}
    )["content"]

    return {
        "schemaVersion": "1.0",
        "recordType": "RESEARCH_PAPER",
        "title": title,
        "authors": authors,
        "paper_url": paper_url,
        "github_url": None,
        "github_stars": None,
        "published_date": published
    }


#url = "https://arxiv.org/abs/1706.03762"

#result = get_paper_info(url)

#print(result)