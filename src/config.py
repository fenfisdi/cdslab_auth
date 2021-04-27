from dotenv import dotenv_values

settings = dotenv_values(".env")
secrets = dotenv_values(".secrets")
email_config = dotenv_values('.email_config')

fastApiConfig = {
    'title': 'cdslab auth',
    'version': '1.0.0',
}
