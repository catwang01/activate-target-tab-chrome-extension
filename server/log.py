import logging
from pathlib import Path
from typing import Optional
import yaml # type: ignore
import logging.config

this_dir = Path(__file__).parent

__IS_LOAD = False

def setupLogger(loggerName: str, configuration_file: Optional[str]=None, default_level=logging.INFO):
    global __IS_LOAD
    configuration_file_path: Path
    if configuration_file is None:
        configuration_file_path = this_dir / "logging.yaml"
    elif isinstance(configuration_file, str):
        configuration_file_path = Path(configuration_file)
    if not __IS_LOAD:
        if configuration_file_path.exists():
            with open(configuration_file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
            __IS_LOAD = True
        else:
            logging.basicConfig(level=default_level)
    return logging.getLogger(loggerName)