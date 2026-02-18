import os
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[4]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

API_HOST = os.getenv("ONETRAINER_API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("ONETRAINER_API_PORT", "8011"))

_DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"
_raw_cors_origins = os.getenv("ONETRAINER_API_CORS_ORIGINS", _DEFAULT_CORS_ORIGINS)
CORS_ORIGINS = [origin.strip() for origin in _raw_cors_origins.split(",") if origin.strip()]
