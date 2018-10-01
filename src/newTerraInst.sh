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
ip=terraform output ip

#echo "storing instance details..."
# store the data
#aws --profile $account --region $region ec2 describe-instances --instance-ids $id > instance-details.json
 
# SSH
# wait from: https://stackoverflow.com/questions/11904772/how-to-create-a-loop-in-bash-that-is-waiting-for-a-webserver-to-respond
echo "Waiting for instance at $ip to become responsive."
until $(curl --output /dev/null --silent --head --fail $ip); do
    printf '.'
    sleep 5
done
 echo "SSH-ing into instance at $ip to prepare and run script"
ssh -i ~/.ssh/terraformer.pem ubuntu@ec2-54-85-128-241.compute-1.amazonaws.com

# # Python from: https://askubuntu.com/questions/101591/how-do-i-install-the-latest-python-2-7-x-or-3-x-on-ubuntu
# sudo apt-get install build-essential checkinstall
# sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
# version=2.7.13
# cd ~/Downloads/
# wget https://www.python.org/ftp/python/$version/Python-$version.tgz
# tar -xvf Python-$version.tgz
# cd Python-$version
# ./configure
# make
# sudo checkinstall

# # Dowload & run script
# #TODO install git 
# mkdir scrape #check path
# cd scrape
# git clone #url
# python src/scraper

# # Send logs to right place & logout
# scpy #send to right folder
# logout

# echo #log

# echo "Terminating instance with prejudice."
# terraform destroy -auto-approve