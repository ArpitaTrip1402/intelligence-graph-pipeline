import aiohttp
from src.crawlers.retry import retry_with_backoff


async def search_github_repository(session, query):

    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc"
    }

    async def make_request():

        async with session.get(
            url,
            params=params,
            timeout=aiohttp.ClientTimeout(total=15)
        ) as response:

            # Rate limit
            if response.status == 429:
                raise Exception("GitHub API rate limit (429)")

            # Temporary server errors
            if response.status >= 500:
                raise Exception(
                    f"GitHub server error ({response.status})"
                )

            # Other errors
            if response.status != 200:
                return None

            return await response.json()

    data = await retry_with_backoff(
        make_request,
        retries=3,
        base_delay=1
    )

    if not data or not data.get("items"):
        return None

    repo = data["items"][0]

    return {
        "name": repo["full_name"],
        "url": repo["html_url"],
        "stars": repo["stargazers_count"],
        "description": repo["description"]
    }