from ..core.store import store
from ..mappers.data import apply_data_settings, to_data_settings
from ..schemas import DataConfigResponse, DataSettings


def get_data_config() -> DataConfigResponse:
    config = store.load()
    return DataConfigResponse(data=to_data_settings(config))


def save_data_config(settings: DataSettings) -> DataConfigResponse:
    config = store.load()
    config = apply_data_settings(config, settings)
    store.save(config)
    return DataConfigResponse(data=to_data_settings(config))
