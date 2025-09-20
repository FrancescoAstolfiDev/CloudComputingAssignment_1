from typing import ClassVar
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

#root path to the project directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, "..", ".env")
env_file_path = os.path.abspath(env_file_path)
print(f"Using .env file: {env_file_path}")

class Settings(BaseSettings):
    app_name: str
    db_address : str  # URL for the db
    modelconfig: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=env_file_path)

#the settings object based on the env_file
settings = Settings(_env_file=env_file_path)


if __name__ == "__main__":
    print("app_name:", settings.app_name)