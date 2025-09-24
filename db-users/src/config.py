from typing import ClassVar

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

#absolute path to the project directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, "..", ".env")
env_file_path = os.path.abspath(env_file_path)
print(f"Using .env file: {env_file_path}")

class Settings(BaseSettings):
    app_name: str = "DefaultApp"  # fallback se .env non viene letto
    mongodb_username: str
    mongodb_password: SecretStr
    mongodb_cluster: str
    mongodb_db: str
    modelconfig: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=env_file_path)

# Settings() use the .env file if no ENV vars are set
# otherway use the ENV vars
settings = Settings(_env_file=env_file_path)




if __name__ == "__main__":
    print("app_name:", settings.app_name)