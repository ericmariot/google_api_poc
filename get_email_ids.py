from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying scopes, delete token.json to re-authenticate
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = Path("token.json")
CREDENTIALS_FILE = Path("credentials.json")
DEFAULT_MAX_RESULTS = 5


def get_credentials() -> Credentials:
    """
    Authenticate and return valid Gmail API credentials.

    Uses existing token if available and valid, otherwise prompts for OAuth flow.
    Saves refreshed/new tokens for future use.

    Returns:
        Credentials: Authenticated Google API credentials
    """
    creds = None

    # Load existing credentials
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Persist credentials
        TOKEN_FILE.write_text(creds.to_json())

    return creds


def fetch_message_ids(max_results: int = DEFAULT_MAX_RESULTS) -> list[str]:
    """
    Fetch Gmail message IDs for the authenticated user.

    Args:
        max_results: Maximum number of message IDs to retrieve

    Returns:
        List of message ID strings

    Raises:
        HttpError: If the Gmail API request fails
    """
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])
        return [msg["id"] for msg in messages]

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def main() -> None:
    """Main entry point - fetch and display message IDs."""
    message_ids = fetch_message_ids()

    if not message_ids:
        print("No messages found.")
        return

    print(f"Found {len(message_ids)} message(s):")
    for msg_id in message_ids:
        print(f"  - {msg_id}")


if __name__ == "__main__":
    main()
