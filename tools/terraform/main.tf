resource "aws_instance" "pipe-instance" {
  ami             = "ami-e24b7d9d"
  instance_type   = "t2.micro"
  key_name = "terraformer"
  user_data = "${file("~/Insight-Data-Ops/src/scraper_setup.sh")}"

  # Allow AWS infrastructure metadata to propagate.
  #provisioner "local-exec" {
  #  command = "sleep 15"
  #}


 # provisioner "remote-exec" {
 #   inline = [
 #     "sudo echo 'export POSTGRES_HOST=${var.postgres_host}' >> $HOME/.profile",
 #     "sudo echo 'export POSTGRES_USER=${var.aws_secret_key}' >> $HOME/.profile",
 #     "sudo echo 'export POSTGRES_PASSWORD=${var.postgres_password}' >> $HOME/.profile",
 #   ]
 # }

  tags {
    Name = "pipe-instance"
  }
}

output "ip" {
  value = "${aws_instance.pipe-instance.public_ip}"
}
