from fastapi import APIRouter

from ..core.store import store
from ..schemas import DataConfigResponse, DataSettings, SaveDataConfigRequest

router = APIRouter()

DATA_CONFIG_FIELDS = [
    "aspect_ratio_bucketing",
    "latent_caching",
    "clear_cache_before_training",
]


def _to_data_settings(config) -> DataSettings:
    config_dict = config.to_dict()
    return DataSettings.model_validate({k: config_dict[k] for k in DATA_CONFIG_FIELDS})


def _apply_data_settings(config, settings: DataSettings):
    payload = settings.model_dump()
    config.aspect_ratio_bucketing = payload["aspect_ratio_bucketing"]
    config.latent_caching = payload["latent_caching"]
    config.clear_cache_before_training = payload["clear_cache_before_training"]
    return config


@router.get("/api/v1/data-config", response_model=DataConfigResponse)
def get_data_config() -> DataConfigResponse:
    config = store.load()
    return DataConfigResponse(data=_to_data_settings(config))


@router.post("/api/v1/data-config", response_model=DataConfigResponse)
def save_data_config(body: SaveDataConfigRequest) -> DataConfigResponse:
    config = store.load()
    config = _apply_data_settings(config, body.data)
    store.save(config)
    return DataConfigResponse(data=_to_data_settings(config))
