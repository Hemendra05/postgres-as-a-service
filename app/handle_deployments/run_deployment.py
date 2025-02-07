"""

"""

import os
import subprocess
import time

import ansible_runner
from fastapi import HTTPException, status

from app import DeploymentParams, logger

from .utils import update_ansible_vars, update_terraform_vars

ansible_dir = os.path.abspath("./ansible")
ansible_inventory = os.path.join(ansible_dir, "inventory")
playbook = os.path.join(ansible_dir, "postgresql_setup.yml")
terraform_dir = os.path.abspath("./terraform")


def run_deployment(params: DeploymentParams):
    """Run Deployment"""
    try:
        update_terraform_vars(params)
        update_ansible_vars(params)

        logger.info("Terraform Dir: %s", terraform_dir)
        logger.info("Ansible Dir: %s", ansible_dir)

        terraform_cmd = [
            "terraform",
            "apply",
            "-auto-approve",
        ]
        tf_init = subprocess.run(
            ["terraform", "init"],
            cwd=terraform_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        if tf_init.returncode != 0:
            logger.error("Terraform Error: %s", tf_init.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Terraform failed:\n{tf_init.stderr}",
            )
        logger.info("Terraform Output: %s", tf_init.stdout)

        tf_run = subprocess.run(
            terraform_cmd,
            cwd=terraform_dir,
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

        time.sleep(30)
        ans_run = ansible_runner.run(
            private_data_dir=ansible_dir,
            playbook=playbook,
            inventory=ansible_inventory,
            envvars={"ANSIBLE_HOST_KEY_CHECKING": "False"},
        )
        if ans_run.rc != 0:
            logger.warning("Retrying Ansible")
            time.sleep(30)
            ans_run = ansible_runner.run(
                private_data_dir=ansible_dir,
                playbook=playbook,
                inventory=ansible_inventory,
                envvars={"ANSIBLE_HOST_KEY_CHECKING": "False"},
            )
            if ans_run.rc != 0:
                logger.error("Ansible Error: %s", ans_run.stderr)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Ansible failed:\n{ans_run.stderr}",
                )
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
