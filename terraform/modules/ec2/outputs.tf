output "primary_public_ip" {
  description = "Public IP of the primary PostgreSQL instance"
  value       = aws_instance.postgres_primary[*].public_ip
}


output "replica_public_ips" {
  description = "Public IPs of the replica PostgreSQL instances"
  value       = aws_instance.postgres_replica[*].public_ip
}
