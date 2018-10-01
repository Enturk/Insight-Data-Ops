resource "aws_instance" "pipe-instance" {
  ami             = "${data.aws_ami.ubuntu.id}"
  instance_type   = "t2.micro"
  key_name = "terraformer"
  tags {
    Name = "pipe-instance"
  }
}

output "ip" {
  value = "${aws_instance.pipe-instance.public_ip}"
}