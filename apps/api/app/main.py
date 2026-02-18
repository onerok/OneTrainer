from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import CORS_ORIGINS
from .routes.backup import router as backup_router
from .routes.concepts import router as concepts_router
from .routes.data import router as data_router
from .routes.general import router as general_router
from .routes.lora import router as lora_router
from .routes.model import router as model_router
from .routes.sampling import router as sampling_router
from .routes.tools import router as tools_router
from .routes.training import router as training_router

app = FastAPI(title="OneTrainer Web API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_router)
app.include_router(model_router)
app.include_router(lora_router)
app.include_router(data_router)
app.include_router(backup_router)
app.include_router(sampling_router)
app.include_router(training_router)
app.include_router(concepts_router)
app.include_router(tools_router)
