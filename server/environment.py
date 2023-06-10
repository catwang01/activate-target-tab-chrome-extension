import os
from dataclasses import dataclass

@dataclass
class EnviromentVariables:
    targetUrl: str

    @classmethod
    def _get_required_environment_variabls(cls, key: str):
        value = os.getenv(key)
        if value is None:
            raise Exception(f"Missing required environment variable: {key}")
        return value

    @classmethod
    def create(cls) -> 'EnviromentVariables':
        targetUrl = cls._get_required_environment_variabls("TARGET_URL")
        obj = cls(targetUrl)
        return obj

global_environ = EnviromentVariables.create()