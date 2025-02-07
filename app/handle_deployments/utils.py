"""

"""


def update_terraform_vars(params):
    """Update Terraform Vars"""
    tf_content = f"""aws_region = "{params.aws_region}"
ami_id = "ami-0025f9fcfdae2458c"
availability_zones = ["ap-south-1a"]
project = "{params.project_name}"
vpc_cidr = "{params.vpc_cidr}"
public_subnets = {params.public_subnets}
allowed_cidr_blocks = {params.allowed_cidr_blocks}
""".replace(
        "'", '"'
    )

    with open("terraform/terraform.tfvars", "w") as tf_file:
        tf_file.write(tf_content)


def update_ansible_vars(params):
    """Update Ansible vars"""
    ansible_content = f"""postgresql_version: {params.postgres_version}
replication_user: {params.replication_username}
replication_password: {params.replication_password}
"""

    with open("ansible/vars/main.yml", "w") as ans_file:
        ans_file.write(ansible_content)
