from ..schemas import DataSettings

DATA_CONFIG_FIELDS = [
    "aspect_ratio_bucketing",
    "latent_caching",
    "clear_cache_before_training",
]


def to_data_settings(config) -> DataSettings:
    config_dict = config.to_dict()
    return DataSettings.model_validate({k: config_dict[k] for k in DATA_CONFIG_FIELDS})


def apply_data_settings(config, settings: DataSettings):
    payload = settings.model_dump()
    config.aspect_ratio_bucketing = payload["aspect_ratio_bucketing"]
    config.latent_caching = payload["latent_caching"]
    config.clear_cache_before_training = payload["clear_cache_before_training"]
    return config
