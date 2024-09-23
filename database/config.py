from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    POSTGRES_HOST: str
    POSTGRES_PORT_CONTAINER: int
    POSTGRES_PORT_HOST: int

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT_CONTAINER}/{self.POSTGRES_DATABASE}'

    @property
    def DATABASE_URL_psycopg(self):
        return f'postgresql+psycopg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT_CONTAINER}/{self.POSTGRES_DATABASE}'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
