# Gmail API POC - Email Content Retrieval

A proof-of-concept project demonstrating how to authenticate with Google's Gmail API and retrieve email content programmatically using Python. This POC provides two core functionalities: listing recent email IDs and fetching full email details by ID.

## Overview

This project showcases:
- OAuth 2.0 authentication flow with Gmail API
- Retrieving email message IDs from a Gmail account
- Fetching complete email details including headers and body content
- Handling multipart MIME messages and base64-encoded content
- Token management and automatic credential refresh

## Prerequisites

- **Python**: 3.11 or higher
- **Poetry**: Python package manager ([installation guide](https://python-poetry.org/docs/#installation))
- **Google Cloud Project**: With Gmail API enabled
- **OAuth 2.0 Credentials**: Downloaded from [Google Cloud Console](https://console.cloud.google.com/apis/api/gmail.googleapis.com/metrics?project=diesel-acolyte-478014-j1&pli=1)

## Setup

### 1. Install Dependencies
- `poetry install`

### 2. Configure Google Cloud Project
- Go to Google Cloud Console
- Create a new project or select an existing one
- Enable the Gmail API:
- Navigate to "APIs & Services" > "Library"
- Search for "Gmail API"
- Click "Enable"

### 3. Create OAuth 2.0 Credentials
- Go to "APIs & Services" > "Credentials"
- Click "Create Credentials" > "OAuth client ID"
- Choose "Desktop app" as the application type
- Download the credentials JSON file
- Save it as `credentials.json` in the project root directory

### 4. Project Structure
google_api_poc/
- credentials.json - OAuth 2.0 credentials (you provide)
- token.json - Auto-generated after first auth
- get_email_ids.py
- get_email_by_id.py
- pyproject.toml

## Authentication
The first time you run either script, an authentication flow will automatically trigger:
A browser window will open asking you to sign in to your Google account
Grant the requested permissions (read-only access to Gmail)
A token.json file will be created to store your credentials
Subsequent runs will use the saved token automatically
Note: If you modify the OAuth scopes in the code, delete token.json to re-authenticate with the new permissions.

## Available Commands
### List Recent Email IDs
```sh
$ poetry run python get_email_ids.py
Found 5 message(s):
  - 19a79834a2c55cc6
  - 19a79807f650c42c
  - 19a797867baa79b2
  - 19a7975fc80b1c46
  - 19a7971d4de42234
```

### Fetch Email by ID
```sh
$ poetry run python get_email_by_id.py -e <EMAIL_ID>

$ poetry run python get_email_by_id.py -e 19a79834a2c55cc6
Fetching email with ID: 19a79834a2c55cc6

================================================================================
Message ID: 19a79834a2c55cc6
Thread ID:  19a4b7f4cdd9b941
================================================================================
From:    Eric Mariot <eric.mariot@email.com>
To:      Eric Mariot <eric.mariot@email.com>
Date:    Wed, 12 Nov 2025 16:20:37 -0300
Subject: Fwd: [ENGINEERING TEST] Rush Certificate Request - TRUCKING LLC MC123456
--------------------------------------------------------------------------------
Body:
[Email body content here...]
```

### Security Notes
Never commit credentials.json or token.json to version control
The OAuth scopes are read-only (gmail.readonly) for safety