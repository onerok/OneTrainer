from enum import Enum

from pydantic import BaseModel


class ToolActionTypeValue(str, Enum):
    WEB_LINK = "WEB_LINK"
    CLI_COMMAND = "CLI_COMMAND"
    INFO = "INFO"


class ToolInfo(BaseModel):
    id: str
    name: str
    description: str
    action_type: ToolActionTypeValue
    action_value: str
    desktop_equivalent: bool


class ToolsConfigResponse(BaseModel):
    data: dict[str, list[ToolInfo]]
