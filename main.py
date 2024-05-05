from phe import paillier
import os

def read_input_from_azure_repo(repo_path):
    # Your logic to read input from Azure Repos
    pass

def write_output_to_azure_blob(ciphertexts, container_client):
    for ctxt in ciphertexts:
        container_client.upload_blob(name=str(ctxt.ciphertext()), data=str(ctxt.ciphertext()))

def main(input_repo_path, connection_string, container_name):
    # Generate keypair
    public_key, private_key = paillier.generate_paillier_keypair()

    # Read plaintext values from Azure Repos
    plaintext_values = read_input_from_azure_repo(input_repo_path)

    # Encrypt plaintext values
    ciphertexts = [public_key.encrypt(plaintext) for plaintext in plaintext_values]

    # Write encrypted results to Azure Blob Storage
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    write_output_to_azure_blob(ciphertexts, container_client)

    # Print decryption results (optional)
    # Perform addition homomorphically
    ctxt_sum = sum(ciphertexts)
    decrypted_sum = private_key.decrypt(ctxt_sum)
    print("Decrypted sum:", decrypted_sum)

if __name__ == "__main__":
    input_repo_path = "path/to/input/repo"  # Path to Azure Repos
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")  # Get Azure Storage connection string from environment variable
    container_name = "your-container-name"  # Azure Blob Storage container name
    main(input_repo_path, connection_string, container_name)
