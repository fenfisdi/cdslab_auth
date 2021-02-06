from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

host = os.getenv('HOST')
port = os.getenv('PORT')