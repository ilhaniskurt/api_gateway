from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    broker_address: str = Field(..., env='BROKER_ADDRESS')
    kafka_login_topic: str = 'login_requests'
    kafka_two_fa_topic: str = 'two_fa_requests'
    kafka_customer_list: str = 'customer_list'
    kafka_customer_connect: str = 'customer_connect'
    kafka_transaction: str = 'transaction'

    cuzdan_api_base_url: str = Field(..., env='CUZDAN_API_BASE_URL')
    cuzdan_login_api: str = Field(..., env='CUZDAN_LOGIN')
    cuzdan_two_factor_api: str = Field(..., env='CUZDAN_TWO_FACTOR')
    cuzdan_customer_list_api: str = Field(..., env='CUZDAN_CUSTOMER_LIST')
    cuzdan_customer_connect_api: str = Field(..., env='CUZDAN_CUSTOMER_CONNECT')
    cuzdan_trasnaction_api: str = Field(..., env='CUZDAN_TRANSACTION')

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()