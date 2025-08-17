import requests
import base64
import json

def create_github_file():
    """
    Prompts the user for information and creates a new file in a GitHub repository.
    """
    # --- 1. Gather User Input ---
    token = input("Enter your GitHub Personal Access Token: ")
    owner = input("Enter the repository owner (e.g., octocat): ")
    repo = input("Enter the repository name (e.g., Hello-World): ")
    path = input("Enter the full path for the new file (e.g., src/new_file.py): ")
    branch = input("Enter the branch name (e.g., main): ")
    message = input("Enter the commit message: ")
    
    print("Enter the file content. Press Ctrl+D (or Ctrl+Z on Windows) when you are finished.")
    content_lines = []
    while True:
        try:
            line = input()
            content_lines.append(line)
        except EOFError:
            break
    content = "\n".join(content_lines)

    # --- 2. Prepare the API Request ---
    
    # The API endpoint URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    # Base64 encode the file content, as required by the GitHub API
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # The data payload for the request
    data = {
        "message": message,
        "content": encoded_content,
        "branch": branch
    }

    # The headers for authentication and API versioning
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # --- 3. Make the API Call ---
    print("\nAttempting to create file...")
    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # This will raise an exception for HTTP error codes (4xx or 5xx)

        # --- 4. Handle the Response ---
        response_data = response.json()
        file_url = response_data.get('content', {}).get('html_url', 'URL not found')
        
        print("\n✅ Success!")
        print(f"File created successfully at: {file_url}")

    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        print(f"\n❌ Error: Failed to create file. Status Code: {status_code}")
        
        if status_code == 401:
            print("   Reason: Authentication failed. Please check your Personal Access Token.")
        elif status_code == 404:
            print("   Reason: Repository not found. Please check the owner and repo name.")
        elif status_code == 422:
            print("   Reason: Validation failed. The file might already exist on this branch, or the branch may not exist.")
        elif status_code == 403:
             print("   Reason: Resource not accessible by this token. Please check your token's permissions.")
        else:
            print(f"   Response from server: {err.response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    create_github_file()
