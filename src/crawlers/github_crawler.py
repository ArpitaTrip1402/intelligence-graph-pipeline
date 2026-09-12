import requests

url = "https://api.github.com/repos/karpathy/nanoGPT"

def get_github_info(repo_url):

    # Convert GitHub URL to GitHub API URL
    api_url = repo_url.replace(
        "https://github.com/",
        "https://api.github.com/repos/"
    )
    response= requests.get(api_url)

    if response.status_code !=200:
        print("Failed to fetch repository")
        print("Status:", response.status_code)
        return None
    
    data=response.json()

    return {
      "Repository":data["name"],
      "Github URL": data["html_url"],
      "Stars": data["stargazers_count"],
      "description": data["description"]
    }

#response = requests.get(url)

#repo_url = "https://github.com/jadore801120/attention-is-all-you-need-pytorch"


#result= get_github_info(repo_url)

#print (result)
# the exact star count change over time , which is why we fetch it dynamically