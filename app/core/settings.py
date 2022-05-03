from pydantic import BaseSettings


class AppSettings(BaseSettings):
    logger_name: str
    logger_level: str

    db_url: str
    db_url_testing: str

    authjwt_secret_key: str = 'secret'
    authjwt_access_token_expires: int = 60 * 60 * 24 * 7
    authjwt_refresh_token_expires: int = 60 * 60 * 24 * 30

    class Config:
        env_file = 'app/core/.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
