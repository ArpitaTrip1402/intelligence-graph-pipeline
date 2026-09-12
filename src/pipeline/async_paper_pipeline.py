import asyncio
import aiohttp

from src.crawlers.async_paper_crawler import get_paper_info
from src.crawlers.async_github_crawler import search_github_repository


async def process_paper(session, paper_url):

    # Step 1: Get paper information
    paper = await get_paper_info(session, paper_url)

    if paper is None:
        return None

    # Step 2: Search GitHub using paper title
    github_repo = await search_github_repository(
        session,
        paper["title"]
    )

    # Step 3: Add GitHub information
    if github_repo is not None:
        paper["github_url"] = github_repo["url"]
        paper["github_stars"] = github_repo["stars"]

    return paper


async def run_pipeline(paper_urls):

    # Limit concurrent connections
    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(
        connector=connector
    ) as session:

        tasks = [
            process_paper(session, url)
            for url in paper_urls
        ]

        results = await asyncio.gather(*tasks)

    return [
        result
        for result in results
        if result is not None
    ]


async def main():

    paper_urls = [
        "https://arxiv.org/abs/1706.03762",
        "https://arxiv.org/abs/1810.04805",
        "https://arxiv.org/abs/2005.14165",
        "https://arxiv.org/abs/2106.09685",
        "https://arxiv.org/abs/2201.11903"
    ]

    results = await run_pipeline(paper_urls)

    print(f"\nSuccessfully processed: {len(results)} papers\n")

    for paper in results:

        print("Title:", paper["title"])
        print("GitHub:", paper["github_url"])
        print("Stars:", paper["github_stars"])
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())