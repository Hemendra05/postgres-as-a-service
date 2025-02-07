"""

"""

import logging

from fastapi import BackgroundTasks, FastAPI

from app import DeploymentParams
from app.handle_deployments import run_deployment, run_destroy

logger = logging.getLogger()

logger.setLevel(logging.INFO)


app = FastAPI(
    title="PostGres Configure APIs",
    root_path="/api/v1",
    version="1.0",
    docs_url=None,
    redoc_url="/documentation",
    contact={
        "name": "PaaS",
        "email": "hemendrachaudhary2052000@gmail.com",
    },
)


@app.post("/deploy")
async def deploy(params: DeploymentParams, background_tasks: BackgroundTasks):
    """Deploy Postgres"""
    background_tasks.add_task(run_deployment, params)
    return {"status": "Deployment initiated"}


@app.post("/destroy")
async def destroy(background_tasks: BackgroundTasks):
    """Destroy Postgres"""
    background_tasks.add_task(run_destroy)
    return {"status": "Destroy initiated"}
