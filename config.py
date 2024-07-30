from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to hold configuration values.

    Attributes:
        HOST (str): The host address for the application.
        PORT (int): The port number for the application.
        DEBUG (bool): Flag to enable or disable debug mode.
        ALLOWED_ORIGINS (list): List of allowed origins for CORS.

    Config:
        env_file (str): Path to the environment file.
    """
    HOST: str = "0.0.0.0"
    PORT: int = 7777
    DEBUG: bool = True
    ALLOWED_ORIGINS: list = ["http://localhost", "http://localhost:8000"]

    class Config:
        """
        Configuration class for the Settings.

        Attributes:
            env_file (str): Path to the environment file.
        """
        env_file = ".env"
