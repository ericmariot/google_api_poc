"""Gmail API client for fetching full email details by ID."""

import argparse
import base64
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = Path("token.json")
CREDENTIALS_FILE = Path("credentials.json")


def get_credentials() -> Credentials:
    """
    Authenticate and return valid Gmail API credentials.

    Uses existing token if available and valid, otherwise prompts for OAuth flow.
    Saves refreshed/new tokens for future use.

    Returns:
        Credentials: Authenticated Google API credentials
    """
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())

    return creds


def get_header_value(headers: list[dict], name: str) -> Optional[str]:
    """
    Extract a specific header value from email headers.

    Args:
        headers: List of header dictionaries
        name: Header name to search for (e.g., 'Subject', 'From')

    Returns:
        Header value if found, None otherwise
    """
    return next(
        (h["value"] for h in headers if h["name"].lower() == name.lower()), None
    )


def decode_body(data: str) -> str:
    """
    Decode base64url-encoded email body.

    Args:
        data: Base64url-encoded string

    Returns:
        Decoded UTF-8 string
    """
    if not data:
        return ""

    try:
        return base64.urlsafe_b64decode(data).decode("utf-8")
    except Exception as e:
        return f"[Error decoding body: {e}]"


def extract_body(payload: dict) -> str:
    """
    Extract email body from message payload.

    Handles both simple messages and multipart MIME messages.

    Args:
        payload: Message payload dictionary

    Returns:
        Decoded email body text
    """
    # Check for multipart message
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                return decode_body(part["body"].get("data", ""))
            elif part["mimeType"] == "text/html" and "parts" not in payload:
                # Fallback to HTML if no plain text
                return decode_body(part["body"].get("data", ""))

    # Simple message (not multipart)
    return decode_body(payload["body"].get("data", ""))


def fetch_email_by_id(email_id: str) -> Optional[dict]:
    """
    Fetch full email details by message ID.

    Args:
        email_id: Gmail message ID

    Returns:
        Dictionary containing email details, or None if error occurs

    Raises:
        HttpError: If the Gmail API request fails
    """
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    try:
        message = (
            service.users()
            .messages()
            .get(userId="me", id=email_id, format="full")
            .execute()
        )

        headers = message["payload"]["headers"]

        return {
            "id": message["id"],
            "thread_id": message.get("threadId"),
            "subject": get_header_value(headers, "Subject") or "[No Subject]",
            "from": get_header_value(headers, "From") or "[Unknown Sender]",
            "to": get_header_value(headers, "To") or "[Unknown Recipient]",
            "date": get_header_value(headers, "Date") or "[Unknown Date]",
            "body": extract_body(message["payload"]),
            "snippet": message.get("snippet", ""),
        }

    except HttpError as error:
        print(f"Error fetching email: {error}")
        return None


def display_email(email: dict) -> None:
    """
    Pretty-print email details to console.

    Args:
        email: Dictionary containing email details
    """
    print("\n" + "=" * 80)
    print(f"Message ID: {email['id']}")
    print(f"Thread ID:  {email['thread_id']}")
    print("=" * 80)
    print(f"From:    {email['from']}")
    print(f"To:      {email['to']}")
    print(f"Date:    {email['date']}")
    print(f"Subject: {email['subject']}")
    print("-" * 80)
    print("Body:")
    print(email["body"] or "[Empty body]")
    print("=" * 80 + "\n")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Fetch and display a Gmail message by ID"
    )
    parser.add_argument(
        "-e", "--email-id", required=True, help="Gmail message ID to retrieve"
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point - fetch and display email by ID."""
    args = parse_arguments()

    print(f"Fetching email with ID: {args.email_id}")

    email = fetch_email_by_id(args.email_id)

    if email:
        display_email(email)
    else:
        print("Failed to retrieve email.")


if __name__ == "__main__":
    main()
