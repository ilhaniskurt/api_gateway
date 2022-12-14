from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    broker_address: str = Field(..., env='BROKER_ADDRESS')
    kafka_login_topic: str = 'login_requests'
    kafka_two_fa_topic: str = 'two_fa_requests'

    cuzdan_api_base_url: str = Field(..., env='CUZDAN_API_BASE_URL')
    cuzdan_login_api: str = Field(..., env='CUZDAN_LOGIN')
    cuzdan_two_factor_api: str = Field(..., env='CUZDAN_TWO_FACTOR')

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()