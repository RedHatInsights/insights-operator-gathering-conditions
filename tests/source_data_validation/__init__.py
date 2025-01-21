from os import path
from pathlib import Path

_FOLDER: Path = Path(path.abspath(__file__)).parent
_PROJECT_ROOT: Path = _FOLDER.parent.parent

CONTAINER_LOG_REQUESTS: Path = _PROJECT_ROOT / "container_log_requests"
