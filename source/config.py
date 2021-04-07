from dotenv import load_dotenv, dotenv_values

settings = dotenv_values(".env")
secrets = dotenv_values(".secrets")
db_config = dotenv_values(".db_config")
qr_config = dotenv_values('.qr_config')
email_config = dotenv_values('.email_config')
