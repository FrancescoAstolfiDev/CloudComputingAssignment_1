from typing import ClassVar
import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Percorso assoluto del file .env nella root del progetto
current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, "..", ".env")
env_file_path = os.path.abspath(env_file_path)
print(f"Using .env file: {env_file_path}")

class Settings(BaseSettings):
    app_name: str   # fallback se .env non viene letto
    db_address : str  # URL del tuo DB service
    modelconfig: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=env_file_path)

# Forziamo la lettura del .env
settings = Settings(_env_file=env_file_path)




if __name__ == "__main__":
    print("app_name:", settings.app_name)