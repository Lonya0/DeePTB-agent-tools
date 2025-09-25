import os
from dotenv import load_dotenv
from dp.agent.adapter.adk import CalculationMCPToolset
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import nest_asyncio
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams

"""
to run a local adk, you need to install: LiteLlm, google-adk
then run `adk web --port 50002 --host 0.0.0.0` outside this directory
"""

load_dotenv()
nest_asyncio.apply()

os.environ['DEEPSEEK_API_KEY'] = os.getenv("DEEPSEEK_API_KEY")

# Global Configuration
BOHRIUM_EXECUTOR = {
    "type": "dispatcher",
    "machine": {
        "batch_type": "Bohrium",
        "context_type": "Bohrium",
        "remote_profile": {
            "email": os.getenv("BOHRIUM_EMAIL"),
            "password": os.getenv("BOHRIUM_PASSWORD"),
            "program_id": int(os.getenv("BOHRIUM_PROJECT_ID")),
            "input_data": {
                "image_name": "registry.dp.tech/dptech/dp/native/prod-19853/dpa-mcp:0.0.0",
                "job_type": "container",
                "platform": "ali",
                "scass_type": "1 * NVIDIA V100_32g"
            }
        }
    }
}
LOCAL_EXECUTOR = {
    "type": "local"
}
BOHRIUM_STORAGE = {
    "type": "bohrium",
    "username": os.getenv("BOHRIUM_EMAIL"),
    "password": os.getenv("BOHRIUM_PASSWORD"),
    "project_id": int(os.getenv("BOHRIUM_PROJECT_ID"))
}

mcp_tools = CalculationMCPToolset(
    connection_params=SseServerParams(url="http://0.0.0.0:50001/sse"),
    storage=BOHRIUM_STORAGE,
    executor=BOHRIUM_EXECUTOR
)

model_config = {
    'model': os.getenv("DEEPSEEK_MODEL_NAME"),
    'api_base': os.getenv("DEEPSEEK_API_BASE"),
    'api_key': os.getenv("DEEPSEEK_API_KEY")
}

root_agent = LlmAgent(
    model=LiteLlm(**model_config),
    name="deeptb_agent",
    description="DeePTB agent to assist on DeePTB tasks.",
    instruction=(
        "You are an expert in materials science and computational chemistry. "
        "Help users execute DeePTB tasks such as generate input config or submit task."
        "Use default parameters if the users do not mention, but let users confirm them before submission. "
        "Always verify the input parameters to users and provide clear explanations of results."
    ),
    tools=[mcp_tools]
)