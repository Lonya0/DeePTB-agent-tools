from pathlib import Path
import importlib
import os
import argparse

from importlib.metadata import version
__version__ = version("dptb_agent")

def load_tools():
    """
    Load all tools from the dptb_agent package.
    """
    module_dir = Path(__file__).parent / "modules"
    
    for py_file in module_dir.glob("*.py"):
        if py_file.name.startswith("_") or py_file.stem in ["utils", "comm"]: 
            continue  # skip __init__.py and utils.py
        
        module_name = f"dptb_agent.modules.{py_file.stem}"
        try:
            module = importlib.import_module(module_name)
            print(f"✅ Successfully loaded: {module_name}")
        except Exception as e:
            print(f"⚠️ Failed to load {module_name}: {str(e)}")


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Dptb Agent Command Line Interface")
    
    parser.add_argument(
        "--transport",
        type=str,
        default=None,
        choices=["sse", "streamable-http"],
        help="Transport protocol to use (default: sse), choices: sse, streamable-http"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        choices=["fastmcp", "test", "dp"],
        help="Model to use (default: dp), choices: fastmcp, test, dp"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to run the MCP server on (default: 50001)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host to run the MCP server on (default: localhost)"
    )
    
    args = parser.parse_args()
    
    return args

def print_address():
    """
    Print the address of the MCP server based on environment variables.
    """
    address = f"{os.environ['DPTB_AGENT_HOST']}:{os.environ['DPTB_AGENT_PORT']}"
    if os.environ["DPTB_AGENT_TRANSPORT"] == "sse":
        print("Address:", address + "/sse")
    elif os.environ["DPTB_AGENT_TRANSPORT"] == "streamable-http":
        print("Address:", address + "/mcp")
    else:
        raise ValueError("Invalid transport protocol specified. Use 'sse' or 'streamable-http'.")

def print_version():
    """
    Print the version of the Dptb_Agent.
    """
    print(f"\nDptb_Agent Tools Version: {__version__}")
    print("For more information, visit: https://github.com/deepmodeling/ABACUS-agent-tools\n")

def main():
    """
    Main function to run the MCP tool.
    """
    print_version()
    args = parse_args()  
    
    from dptb_agent.env import set_envs, create_workpath
    set_envs(
        transport_input=args.transport,
        model_input=args.model,
        port_input=args.port, 
        host_input=args.host)
    create_workpath()

    from dptb_agent.init_mcp import mcp
    load_tools()  

    print_address()
    mcp.run(transport=os.environ["DPTB_AGENT_TRANSPORT"])

if __name__ == "__main__":
    main()
