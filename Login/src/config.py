from typing import ClassVar
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# root path to the project directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, "..", ".env")
env_file_path = os.path.abspath(env_file_path)


class Settings(BaseSettings):
    app_name: str
    db_address: str  # URL for the db

    # carica .env solo se non trovi già variabili d'ambiente
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=env_file_path)

# Settings() usa già le ENV di sistema se presenti,
# altrimenti cade in fallback sul .env
settings = Settings()

if __name__ == "__main__":
    print("app_name:", settings.app_name)
    print("db_address:", settings.db_address)
