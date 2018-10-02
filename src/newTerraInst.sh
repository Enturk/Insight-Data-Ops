#!/bin/bash

echo "Configuring and creating Terraform instance... "
# Echo "and the Bunnymen"

# TODO THIS IS BAD AND I FEEL BAD
cd ~/workspace/tools/terraform

# Terraform!
echo 'creating instance...'
#id=$(aws --profile $account --region $region ec2 run-instances --image-id $image_id --count $count --instance-type $instance_type --key-name $ssh_key_name --subnet-id $subnet_id --block-device-mapping "[ { \"DeviceName\": \"/dev/sda1\", \"Ebs\": { \"VolumeSize\": $root_vol_size } } ]" --query 'Instances[*].InstanceId' --output text)
#echo "$id created"
terraform init
terraform plan
terraform apply -auto-approve
ip=$(terraform output ip)

# Running script once on instance: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
# To run on restart, use this: https://aws.amazon.com/premiumsupport/knowledge-center/execute-user-data-ec2/

ip_with_dashes= "$ip" | tr . -
ssh_target=ubuntu@ec2-$ip.compute-1.amazonaws.com

echo "Copy & paste these three lines into one bash command line:"
echo 'ssh -i ~/.ssh/terraformer.pem -o "StrictHostKeyChecking no" '$ssh_target

# echo "Terminating instance with prejudice."
# terraform destroy -auto-approve