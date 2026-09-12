import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def get_paper_info(session, paper_url):

    try:
        async with session.get(
            paper_url,
            timeout=aiohttp.ClientTimeout(total=15)
        ) as response:

            if response.status != 200:
                print(f"Failed: {paper_url} | Status: {response.status}")
                return None

            html = await response.text()

    except Exception as e:
        print(f"Request failed: {paper_url} | {e}")
        return None

    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1", class_="title")
    authors_tag = soup.find("div", class_="authors")
    date_tag = soup.find("meta", {"name": "citation_date"})

    if not title_tag or not authors_tag or not date_tag:
        return None

    title = title_tag.get_text(" ", strip=True)
    title = title.replace("Title:", "").strip()

    authors = authors_tag.get_text(" ", strip=True)
    authors = authors.replace("Authors:", "").replace(":", "").strip()

    published = date_tag.get("content")

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


async def crawl_papers(paper_urls):

    connector = aiohttp.TCPConnector(limit=20)

    async with aiohttp.ClientSession(
        connector=connector
    ) as session:

        tasks = [
            get_paper_info(session, url)
            for url in paper_urls
        ]

        results = await asyncio.gather(*tasks)

    return [result for result in results if result is not None]


if __name__ == "__main__":

    paper_urls = [
        "https://arxiv.org/abs/1706.03762",
        "https://arxiv.org/abs/1810.04805",
        "https://arxiv.org/abs/2005.14165",
        "https://arxiv.org/abs/2106.09685",
        "https://arxiv.org/abs/2201.11903"
    ]

    results = asyncio.run(crawl_papers(paper_urls))

    print(f"\nSuccessfully crawled: {len(results)} papers")

    for paper in results:
        print("\nTitle:", paper["title"])
        print("URL:", paper["paper_url"])