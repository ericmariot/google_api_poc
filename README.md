# [POC] Google API retrieve email content

### Example usage
get_email_ids
```sh
poetry run python get_email_ids.py
Found 5 message(s):
  - 19a79834a2c55cc6
  - 19a79807f650c42c
  - 19a797867baa79b2
  - 19a7975fc80b1c46
  - 19a7971d4de42234
```

get_email_by_id
```sh
poetry run python get_email_by_id.py -e 19a79834a2c55cc6                
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
Eric Mariot
...
```
