from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    yaml_config: str = r"configs\windows.yaml"
