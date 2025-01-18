from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    api_title: str = "Auth Mozgs Delivery API"
    api_description: str = "Api for Auth Mozgs Delivery service"
    api_version: str = "1.0.0"
    debug: bool = False
    sql_alchemy_database_url: str
    jwt_secret_key: str
    jwt_access_token_expires: int
    jwt_algorithm: str = 'HS256'

    class Config:
        env_file = '.env'


settings = Settings()