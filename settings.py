from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

host = os.getenv('HOST')
port = os.getenv('PORT')
domain = os.getenv('DOMAIN')

reload = os.getenv('RELOAD')
access_log = os.getenv('ACCESS_LOG')

applicant_path = os.getenv('APPLICANT_PATH')

print(f'The app is running in domain: {domain}')
