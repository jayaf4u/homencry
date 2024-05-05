from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
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
        return base64.b64decode(content).decode("utf-8")
    else:
        print(f"Failed to read input from GitHub repository. Status code: {response.status_code}")
        return None

def encrypt_data(public_key, plaintext):
    encrypted_value = public_key.encrypt(plaintext)
    return encrypted_value

def upload_blob(storage_connection_string, container_name, file_name, data):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_name)
        
        blob_client.upload_blob(data, overwrite=True)
        print(f"Uploaded encrypted content to Azure Blob Storage: {file_name}")
    except Exception as e:
        print(f"Failed to upload encrypted content to Azure Blob Storage: {e}")

# Example usage
repo_owner = "jayaf4u"  # GitHub repository owner
repo_name = "homencry"  # GitHub repository name
input_file_path = "input.txt"  # Path to input file in the GitHub repository
github_token = "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"  # GitHub personal access token

# Azure Storage details
storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=azstore116;AccountKey=yHj/v4bPhglmtQvHqD7pGAtqF8sMSEVMBYoWYEuZbT3Y6wyhKHNdSOOfAMtU8fKDiBnCxnOtAFqY+AStrKPGxQ==;EndpointSuffix=core.windows.net"  # Replace with your Azure Storage connection string
container_name = "con1"  # Replace with your container name
output_file_name = "output.txt"  # Output file name in Azure Blob Storage

# Fetch input content from GitHub repository
input_content = read_input_from_github_repo(repo_owner, repo_name, input_file_path, github_token)
if input_content:
    # Generate public/private key pair for Paillier encryption
    public_key, _ = paillier.generate_paillier_keypair()
    
    # Encrypt the input content using the public key
    encrypted_content = encrypt_data(public_key, int(input_content))  # Assuming input content is an integer
    
    # Convert encrypted content to bytes
    encrypted_bytes = bytes(' '.join(map(str, encrypted_content.ciphertext())), encoding='utf-8')
    
    # Upload encrypted content to Azure Blob Storage
    upload_blob(storage_connection_string, container_name, output_file_name, encrypted_bytes)
