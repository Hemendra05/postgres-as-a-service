[postgresql_servers]
primary ansible_host=${primary_ip} ansible_user=ubuntu ansible_ssh_private_key_file=./../terraform/keys/paas-key.pem
replica1 ansible_host=${replica1_ip} ansible_user=ubuntu ansible_ssh_private_key_file=./../terraform/keys/paas-key.pem
replica2 ansible_host=${replica2_ip} ansible_user=ubuntu ansible_ssh_private_key_file=./../terraform/keys/paas-key.pem

[primary]
primary

[replicas]
replica1
replica2
