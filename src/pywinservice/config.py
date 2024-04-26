from pydantic_settings import BaseSettings
import yaml
import os
import sys
import platform
class Settings(BaseSettings):
    if platform.system() == "Windows":
        yaml_config: str = r"configs\windows.yaml"
    elif platform.system() == "Linux":
        yaml_config: str = "configs/linux.yaml"
    else:
        yaml_config: str = "configs/default.yaml"


settings = Settings()

def load_config():
    yaml_config = settings.yaml_config
    yaml_config = os.path.join(os.path.dirname(sys.argv[0]), yaml_config)
    config = yaml.safe_load(open(yaml_config))
    return config