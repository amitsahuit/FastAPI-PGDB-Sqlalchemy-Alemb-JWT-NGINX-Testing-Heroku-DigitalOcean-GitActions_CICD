from pydantic import BaseSettings

class Settings(BaseSettings):
    #Database.py Db variables e.g --> postgresql://postgres:sys@localhost:5432/fastapidb1
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str # --> We keept as String because in the DB URL it will pass as string
    DATABASE_HOSTNAME: str = "localhost" # we can provide any default value like this.
    DATABASE_PORT: str # --> We keept as String because in the DB URL it will pass as string
    DATABASE_NAME: str 

    #oAuth2.py JWT variables
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'

setting = Settings()
