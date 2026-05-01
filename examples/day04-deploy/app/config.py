from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # 必填，没有就报错
    dp_api_key:str  
    # 有默认值
    dp_url:str = "https://api.deepseek.com"
    #有默认值
    dp_mode:str = "deepseek-v4-flash"
    # 可选
    al_em_key:str=""
    # 默认值
    al_em_mode:str="text-embedding-v4"
    # 默认值
    al_em_url:str="https://dashscope.aliyuncs.com/compatible-mode/v1"

    model_config = ConfigDict(env_file="../.env")

settings = Settings()