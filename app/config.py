from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str  # Define the database URL to load from the environment file
    # Optionally, you can define other components of the database configuration
    database_username: str
    database_password: str
    database_hostname: str
    database_port: int
    database_name: str

    class Config:
        env_file = ".env"  # Specify the location of the environment file
        env_file_encoding = "utf-8"

# Instantiate the settings class to make it accessible
settings = Settings()
