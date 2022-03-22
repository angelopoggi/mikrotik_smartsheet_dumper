import os
from dotenv import load_dotenv,find_dotenv
from pathlib import Path  # Python 3.6+ only

env_file = find_dotenv()
try:
    load_dotenv(env_file)
except:
    print("Please create a local .env file with local credentials")
    exit()
SMARTSHEET_ACCESS_TOKEN = os.getenv("SMARTSHEET_ACCESS_TOKEN")
MIKROTIK_USERNAME = os.getenv("MIKROTIK_USERNAME")
MIKROTIK_PASSWORD = os.getenv("MIKROTIK_PASSWORD")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")