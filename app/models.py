"""

"""

from typing import List

from pydantic import BaseModel


class DeploymentParams(BaseModel):
    """Deployment Params"""

    postgres_version: int
    replication_username: str
    replication_password: str
    aws_region: str
    project_name: str
    vpc_cidr: str
    public_subnets: List[str]
    allowed_cidr_blocks: List[str]
