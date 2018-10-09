#!/bin/bash

# TODO THIS IS BAD AND I FEEL BAD
cd ~/Insight-Data-Ops/tools/terraform

# Terraform!
echo 'Creating Terraform instance to start with script'
terraform init
terraform plan
terraform apply -auto-approve
ip=$(terraform output ip)

# Running script once on instance: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
# To run on restart, use this: https://aws.amazon.com/premiumsupport/knowledge-center/execute-user-data-ec2/

# ssh helper
ssh_target="ubuntu@ec2-${ip//\./-}.compute-1.amazonaws.com"
echo "Copy & paste this into bash command line to ssh into instance:"
echo 'ssh -i ~/.ssh/terraformer.pem -o "StrictHostKeyChecking no" '$ssh_target

 # Transfer env variables
scp -i ~/.ssh/terraformer.pem -o "StrictHostKeyChecking=no" -o "UserKnownHostsFile=/dev/null" ~/Insight-Data-Ops/.env $ssh_target:/tmp/
# cat ~/.ssh/id_rsa.pub | ssh -o "StrictHostKeyChecking no" $ssh_target 'cat >> ~/.ssh/authorized_keys' &

# need to wait

# echo "Terminating instance with prejudice."
# terraform destroy -auto-approve
