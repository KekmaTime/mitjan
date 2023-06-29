import requests
from zulip import Client

# Zulip bot configuration
BOT_EMAIL = "email"  # Your bot's email address
BOT_API_KEY = "your-bot-api-key"  # Your bot's API key
ZULIP_SITE_URL = "your-zulip-organization.zulipchat.com"  # Your Zulip organization URL

# GitHub repository details
GITHUB_API_URL = " "
GITHUB_OWNER = "github-username"
GITHUB_REPO = "github-repo"

# Fetch pull requests with "workflows awaiting approval" status
def get_pull_requests():
    url = f"{GITHUB_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls"
    response = requests.get(url)
    return response.json()

# Filter pull requests with "workflows awaiting approval" status
def filter_pull_requests(pull_requests):
    filtered_prs = []
    for pr in pull_requests:
        if pr["state"] == "open" and "workflows awaiting approval" in pr["labels"]:
            filtered_prs.append(pr)
    return filtered_prs

# Send Zulip message for the filtered pull requests
def send_zulip_message(filtered_prs):
    zulip_client = Client(site=ZULIP_SITE_URL)
    for pr in filtered_prs:
        zulip_client.send_message({
            "type": "private",
            "to": BOT_EMAIL,
            "content": f"New PR with workflows awaiting approval: {pr['html_url']}"
        })

# Main function
def main():
    pull_requests = get_pull_requests()
    filtered_prs = filter_pull_requests(pull_requests)
    send_zulip_message(filtered_prs)

if __name__ == "__main__":
    main()
