from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.')/'.env_secrets'
load_dotenv(dotenv_path=env_path)

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
access_token_expire_minutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

crypto_context_schem = os.getenv('CRYPTOCONTEXT_SCHEM')
crypto_context_deprecated = os.getenv('CRYPTOCONTEXT_DEPRECATED')


#rint(access_token_expire_minutes)