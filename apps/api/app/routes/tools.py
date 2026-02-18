from fastapi import APIRouter

from ..schemas import ToolActionTypeValue, ToolInfo, ToolsConfigResponse

router = APIRouter()


@router.get("/api/v1/tools-config", response_model=ToolsConfigResponse)
def get_tools_config() -> ToolsConfigResponse:
    tools = [
        ToolInfo(
            id="wiki",
            name="Wiki",
            description="Open OneTrainer documentation.",
            action_type=ToolActionTypeValue.WEB_LINK,
            action_value="https://github.com/Nerogar/OneTrainer/wiki",
            desktop_equivalent=False,
        ),
        ToolInfo(
            id="caption_ui",
            name="Dataset Tools",
            description="Desktop captioning and dataset tooling.",
            action_type=ToolActionTypeValue.CLI_COMMAND,
            action_value="./run-cmd.sh caption_ui",
            desktop_equivalent=True,
        ),
        ToolInfo(
            id="video_tool_ui",
            name="Video Tools",
            description="Desktop video utilities.",
            action_type=ToolActionTypeValue.CLI_COMMAND,
            action_value="./run-cmd.sh video_tool_ui",
            desktop_equivalent=True,
        ),
        ToolInfo(
            id="convert_model_ui",
            name="Convert Model Tools",
            description="Desktop model conversion UI.",
            action_type=ToolActionTypeValue.CLI_COMMAND,
            action_value="./run-cmd.sh convert_model_ui",
            desktop_equivalent=True,
        ),
        ToolInfo(
            id="sample_ui",
            name="Sampling Tool",
            description="Desktop sampling UI.",
            action_type=ToolActionTypeValue.CLI_COMMAND,
            action_value="./run-cmd.sh sample",
            desktop_equivalent=True,
        ),
        ToolInfo(
            id="profiling",
            name="Profiling Tool",
            description="Desktop profiling window.",
            action_type=ToolActionTypeValue.INFO,
            action_value="Available in desktop UI only.",
            desktop_equivalent=True,
        ),
    ]
    return ToolsConfigResponse(data={"tools": tools})
