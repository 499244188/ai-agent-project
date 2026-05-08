from pydantic_settings import BaseSettings
from pydantic import ConfigDict


# 配置
class Settings(BaseSettings):
    dp_api_key:str
    dp_url:str = "https://api.deepseek.com"
    dp_mode:str = "deepseek-v4-pro"
    al_em_key:str
    al_em_mode:str = "text-embedding-v4"
    al_em_url:str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    pg_host:str = "localhost"
    pg_port:int = 5432
    pg_user:str = "postgres"
    pg_password:str = "123456"
    pg_db:str = "postgres"

    model_config = ConfigDict(env_file="../../.env")

settings = Settings()


