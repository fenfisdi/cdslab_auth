from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.')/'.env_secrets'
load_dotenv(dotenv_path=env_path)

