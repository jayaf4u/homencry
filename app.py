from phe import paillier
import base64
import requests

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
        return base64.b64decode(content).decode("utf-8"), response.json()["sha"]
    else:
        print(f"Failed to read input from GitHub repository. Status code: {response.status_code}")
        return None, None

def encrypt_data(public_key, plaintext):
    encrypted_value = public_key.encrypt(plaintext)
    return encrypted_value.ciphertext()

def write_encrypted_content_to_github_repo(repo_owner, repo_name, file_path, content, sha, token=None):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    encrypted_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        "message": "Add encrypted content to output.txt",
        "content": encrypted_content,
        "sha": sha
    }
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Encrypted content successfully pushed to GitHub.")
    else:
        print(f"Failed to push encrypted content to GitHub. Status code: {response.status_code}")

# Example usage
repo_owner = "jayaf4u"  # GitHub repository owner
repo_name = "homencry"  # GitHub repository name
input_file_path = "input.txt"  # Path to input file in the GitHub repository
output_file_path = "output.txt"  # Path to output file in the GitHub repository
github_token = "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"  # GitHub personal access token

# Fetch input content from GitHub repository
input_content, sha = read_input_from_github_repo(repo_owner, repo_name, input_file_path, github_token)
if input_content:
    # Generate public/private key pair for Paillier encryption
    public_key, private_key = paillier.generate_paillier_keypair()
    
    # Encrypt the input content using the public key
    encrypted_content = encrypt_data(public_key, int(input_content))  # Assuming input content is an integer
    
    # Write encrypted content to output.txt file in GitHub repository
    write_encrypted_content_to_github_repo(repo_owner, repo_name, output_file_path, str(encrypted_content), sha, github_token)
