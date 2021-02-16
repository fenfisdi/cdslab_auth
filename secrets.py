from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.')/'.env_secrets'
load_dotenv(dotenv_path=env_path)

crypto_context_schem = os.getenv('CRYPTOCONTEXT_SCHEM')
crypto_context_deprecated = os.getenv('CRYPTOCONTEXT_DEPRECATED')

#print(crypto_context_deprecated)