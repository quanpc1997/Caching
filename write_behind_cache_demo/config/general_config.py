from pydantic_settings import BaseSettings

class ConfigurationManager(BaseSettings):
    fastapi_application_name: str = "QuanPC"
    fastapi_application_title: str = "1.0"
    fastapi_application_description: str = "Write Behind Caching Demo"

    event_id: str = "EV123"

    debug_mode: bool = True

    redis_host: str = "localhost"
    redis_post: int = 6379
    redis_db: str = "0"
    redis_timeout: int = 300

    sqlalchemy_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ecommerce"
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 1800
    pool_recycle: int = 1800

    kafka_bootstrap_server: str = '127.0.0.1:9095'
    reserve_redis_pg_topic: str = "RESERVE_REDIS_PG"
    reserve_result_topic: str = "RESERVE_RESULT"

    class Config:
        env_file = "../config.env"
        case_sensitive = False


config = ConfigurationManager()