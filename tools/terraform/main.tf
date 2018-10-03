resource "aws_instance" "pipe-instance" {
  ami             = "ami-e24b7d9d"
  instance_type   = "t2.micro"
  key_name = "terraformer"
  user_data = "${file("~/Insight-Data-Ops/src/scraper_setup.sh")}"

  tags {
    Name = "pipe-instance"
  }
}

output "ip" {
  value = "${aws_instance.pipe-instance.public_ip}"
}
