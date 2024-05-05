import requests
import base64

def read_input_from_github_repo(repo_owner, repo_name, file_path, token=None):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    # Make a GET request to GitHub API to fetch the file contents
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Decode the content from base64 and return
        content = response.json()["content"]
        return base64.b64decode(content).decode("utf-8")
    else:
        print(f"Failed to read input from GitHub repository. Status code: {response.status_code}")
        return None

# Example usage
repo_owner = "jayaf4u"  # GitHub repository owner
repo_name = "homencry"  # GitHub repository name
file_path = "input.txt"  # Path to input file in the GitHub repository
github_token = "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"  # Optional: GitHub personal access token

input_content = read_input_from_github_repo(repo_owner, repo_name, file_path, github_token)
if input_content:
    print("Input content:", input_content)
