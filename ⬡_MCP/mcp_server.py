from fastapi import FastAPI, HTTPException
from redis import Redis
import yaml
from pathlib import Path
import os

# Initialize FastAPI app
app = FastAPI(title="MCP Server")

# Load configuration
config_path = Path(__file__).parent / "mcp_config.yml"
with open(config_path) as f:
    config = yaml.safe_load(f)

# Initialize Redis connection
redis_client = Redis(
    host=config['redis']['host'],
    port=config['redis']['port'],
    decode_responses=True
)

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis connection failed: {str(e)}")

# Directory status endpoint
@app.get("/directories/status")
async def directory_status():
    status = {}
    for dir_name, dir_path in config['directories'].items():
        expanded_path = os.path.expanduser(dir_path)
        status[dir_name] = {
            "path": expanded_path,
            "exists": os.path.exists(expanded_path),
            "is_directory": os.path.isdir(expanded_path) if os.path.exists(expanded_path) else False
        }
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
