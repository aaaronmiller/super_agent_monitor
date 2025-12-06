from mcp.server.fastmcp import FastMCP
import httpx
import json
import os

# Initialize FastMCP server
mcp = FastMCP("Plan Deployer")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:3001")

@mcp.tool()
def deploy_plan(name: str, prompt: str, description: str = "", files: list[dict] = None, config: dict = None) -> str:
    """
    Deploy a new agent plan (orchestrator) to the .claude directory.
    
    Args:
        name: The name of the plan (will be the folder name).
        prompt: The initial prompt/instructions for the agent (CLAUDE.md).
        description: A brief description of the plan.
        files: Optional list of files to create. Each item should be {"name": "filename.ext", "content": "file content"}.
        config: Optional configuration dictionary for config.json.
    
    Returns:
        The path to the deployed plan directory.
    """
    payload = {
        "name": name,
        "prompt": prompt,
        "description": description,
        "files": files or [],
        "orchestrator_config": config or {}
    }
    
    try:
        response = httpx.post(f"{BACKEND_URL}/api/plans/deploy", json=payload, timeout=10.0)
        response.raise_for_status()
        result = response.json()
        return f"Successfully deployed plan '{name}' to {result['path']}"
    except Exception as e:
        return f"Error deploying plan: {str(e)}"

if __name__ == "__main__":
    mcp.run()
