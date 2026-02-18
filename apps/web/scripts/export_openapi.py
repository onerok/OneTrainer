import json
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from apps.api.app.main import app  # noqa: E402

output_dir = THIS_FILE.parents[1] / "src" / "lib" / "api" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)
openapi_path = output_dir / "openapi.json"

with openapi_path.open("w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)
    f.write("\n")

print(f"wrote {openapi_path}")
