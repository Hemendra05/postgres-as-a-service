"""

"""

import os
import subprocess

from fastapi import HTTPException, status

from app import DeploymentParams, logger

from .utils import update_ansible_vars, update_terraform_vars

ansible_dir = os.path.abspath("./ansible")
ansible_inventory = os.path.join(ansible_dir, "inventory")
playbook = os.path.join(ansible_dir, "postgresql_setup.yml")


def run_deployment(params: DeploymentParams):
    """Run Deployment"""
    try:
        update_terraform_vars(params)
        update_ansible_vars(params)

        # Execute Terraform apply – assuming your working directory is "terraform"
        terraform_cmd = [
            "terraform",
            "apply",
            "-auto-approve",
        ]
        tf_run = subprocess.run(
            terraform_cmd,
            cwd="./terraform",
            capture_output=True,
            text=True,
            check=True,
        )
        if tf_run.returncode != 0:
            logger.error("Terraform Error: %s", tf_run.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Terraform failed:\n{tf_run.stderr}",
            )
        logger.info("Terraform Output: %s", tf_run.stdout)
        ansible_cmd = ansible_cmd = [
            "ansible-playbook",
            "-i",
            ansible_inventory,
            playbook,
        ]
        ans_run = subprocess.run(
            ansible_cmd,
            cwd="./ansible",
            capture_output=True,
            text=True,
            check=True,
            timeout=1000,
        )
        if ans_run.returncode != 0:
            logger.error("Ansible Error: %s", ans_run.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ansible failed:\n{ans_run.stderr}",
            )
        logger.info("Ansible Output: %s", ans_run.stdout)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        ) from e


def run_destroy():
    """Run Destroy"""
    try:
        terraform_cmd = [
            "terraform",
            "destroy",
            "-auto-approve",
        ]
        tf_run = subprocess.run(
            terraform_cmd,
            cwd="./terraform",
            capture_output=True,
            text=True,
            check=True,
        )
        if tf_run.returncode != 0:
            logger.error("Terraform Error: %s", tf_run.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Terraform failed:\n{tf_run.stderr}",
            )
        logger.info("Terraform Output: %s", tf_run.stdout)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        ) from e
