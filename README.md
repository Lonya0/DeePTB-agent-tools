# DeePTB Agent Tools

DeePTB-agent-tools is a Python package that provides the Model Context Protocol (MCP) tools to connect large language models (LLMs) to ABACUS computational jobs. It serves as a bridge between AI models and first principles calculations, enabling intelligent interaction with DeePTB workflows.

This agent's template is borrowed from ABACUS-agent-tools: https://github.com/pxlxingliang/ABACUS-agent-tools

To build a user interface, check out BetterAIM -> https://github.com/Lonya0/BetterAIM

## Installation
To use DeePTB agent tools with Google Agent Development Kit (ADK), follow the recommended installation process:

1. Create and activate a conda enviroment:
```bash
conda create -n dtat python=3.11
conda activate dtat
```
2. Install DeePTB:
follow DeePTB install instruction to install one.

3. Install DeePTB-agent-tools:
```bash
cd ..
git clone https://github.com/Lonya0/DeePTB-agent-tools.git
cd DeePTB-agent-tools
pip install .
```

## Using DeePTB-agent-tools with BetterAIM

### Starting DeePTB-agent-tools

```bash
>>> dtat --host 0.0.0.0 --port 50001
✅ Successfully loaded: dptb_agent_tools.modules
INFO:     Started server process [25487]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:50001 (Press CTRL+C to quit)
```
### Start BetterAIM
visit https://github.com/Lonya0/BetterAIM to get help
above shown url is used in BetterAIM