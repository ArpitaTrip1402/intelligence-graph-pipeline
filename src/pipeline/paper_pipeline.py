import json

from src.crawlers.paper_crawler import get_paper_info
from src.crawlers.github_search import search_github_repository
from src.crawlers.github_crawler import get_github_info


def process_paper(paper_url):

    # Step 1: Get paper information
    paper = get_paper_info(paper_url)

    if paper is None:
        return None

    # Step 2: Search GitHub using paper title
    github_repo = search_github_repository(paper["title"])

    if github_repo is None:
        return paper

    # Step 3: Get detailed GitHub information
    github_info = get_github_info(github_repo["url"])

    if github_info is None:
        return paper

    # Step 4: Add GitHub information to paper
    if github_info is not None:
     paper["github_url"] = github_info["Github URL"]
     paper["github_stars"] = github_info["Stars"]

    return paper

if __name__ == "__main__":

    paper_urls = [
        "https://arxiv.org/abs/1706.03762",
        "https://arxiv.org/abs/1810.04805",
        "https://arxiv.org/abs/2005.14165",
        "https://arxiv.org/abs/2106.09685",
        "https://arxiv.org/abs/2201.11903"
    ]

    results = []


    for url in paper_urls:
        print("Processing:", url)

        result = process_paper(url)

        if result:
            results.append(result)

    # Save results
    with open("data/research_papers.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print("\nTotal papers:", len(results))
    print("Saved to data/research_papers.json")