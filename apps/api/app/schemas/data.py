from pydantic import BaseModel


class DataSettings(BaseModel):
    aspect_ratio_bucketing: bool
    latent_caching: bool
    clear_cache_before_training: bool


class DataConfigResponse(BaseModel):
    data: DataSettings


class SaveDataConfigRequest(BaseModel):
    data: DataSettings
