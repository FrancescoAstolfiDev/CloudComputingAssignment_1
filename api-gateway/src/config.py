from typing import ClassVar
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# root path to the project directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, "..", ".env")
env_file_path = os.path.abspath(env_file_path)

print(f"Using .env file (only if no ENV vars are set): {env_file_path}")

class Settings(BaseSettings):
    app_name: str
    login_address: str
    homepage_address: str

    # carica .env solo se non trovi già variabili d'ambiente
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=env_file_path)

# Settings() usa già le ENV di sistema se presenti,
# altrimenti cade in fallback sul .env
settings = Settings()

