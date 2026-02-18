import json
from pathlib import Path

from .settings import REPO_ROOT

from modules.util.config.TrainConfig import TrainConfig  # noqa: E402


class ConfigStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.config_path = repo_root / "training_user_settings" / "web-general-config.json"

    def load(self) -> TrainConfig:
        config = TrainConfig.default_values()
        if self.config_path.exists():
            with self.config_path.open("r", encoding="utf-8") as f:
                config.from_dict(json.load(f))
        return config

    def save(self, config: TrainConfig) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w", encoding="utf-8") as f:
            json.dump(config.to_dict(), f, indent=2)
            f.write("\n")


def resolve_repo_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


store = ConfigStore(REPO_ROOT)
