from pydantic_settings import BaseSettings
import platform
class Settings(BaseSettings):
    if platform.system() == 'Linux':
        yaml_config: str = r"configs/linux.yaml"
    elif platform.system() == 'Windows':
        yaml_config: str = r"configs/windows.yaml"
