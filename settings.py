from dotenv import load_dotenv
import os

load_dotenv(find_dotenv())

host = os.environ("HOST")
port = os.environ("PORT")