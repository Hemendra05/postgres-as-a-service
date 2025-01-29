output "primary_public_ip" {
  description = "Public IP of the primary PostgreSQL instance"
  value       = module.ec2.primary_public_ip
}


output "replica_public_ips" {
  description = "Private IPs of the replica PostgreSQL instances"
  value       = module.ec2.replica_public_ips
}
