import requests
import re

def normalize_text(text):
    """Convert text into a simple comparable format."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text



def search_github_repository(query):

    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "sort":"stars",
        "order" :"desc"
    }

    try:
     response = requests.get(
        url,
        params=params,
        timeout=10
     )
    except requests.RequestException as e:
     print("GitHub request failed:", e)
     return None

    if response.status_code != 200:
        print("GitHub search failed")
        print("Status:",response.status_code)
        return None

    data = response.json()

    if not data["items"]:
        return None
    
    paper_title = normalize_text(query)

    # Check candidate repositories
    for repo in data["items"][:10]:

        repo_name = normalize_text(repo["name"])
        description = normalize_text(repo["description"] or "")

        # Check whether important words from paper title
        # appear in repository name or description
        title_words = paper_title.split()

        matching_words = 0

        for word in title_words:
            if len(word) > 2:
                if word in repo_name or word in description:
                    matching_words += 1

        # Require reasonable evidence of relevance
        if matching_words >= max(2, len(title_words) // 2):

          return {
        "name": repo["full_name"],
        "url": repo["html_url"],
        "stars": repo["stargazers_count"],
        "description": repo["description"]
    }

# Test

    return None



    

