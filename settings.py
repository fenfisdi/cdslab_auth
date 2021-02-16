from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

host = os.getenv('HOST')
port = os.getenv('PORT')
domain = os.getenv('DOMAIN')
applicant_path = os.getenv('APPLICANT_PATH')

#print(applicant_path)
