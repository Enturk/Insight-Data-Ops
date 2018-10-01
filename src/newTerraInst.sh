#!/bin/bash

echo "Configuring and creating Terraform instance... "
# Echo "and the Bunnymen"

# Global Settings
account="my-account"
region="us-east-1"

# Instance settings
image_id="ami-66ca1419" # ubuntu 16.04 ebs-hvm-ena
ssh_key_name="my_ssh_key-rsa-2048"
instance_type="t2.micro"
subnet_id="subnet-4a7cfc16"
root_vol_size=20
count=1

# Terraform!
id=$(aws --profile $account --region $region ec2 run-instances --image-id $image_id --count $count --instance-type $instance_type --key-name $ssh_key_name --subnet-id $subnet_id --block-device-mapping "[ { \"DeviceName\": \"/dev/sda1\", \"Ebs\": { \"VolumeSize\": $root_vol_size } } ]" --query 'Instances[*].InstanceId' --output text)
echo "$id created"

# Store the data
echo "storing instance details in instance-details.json"
aws --profile $account --region $region ec2 describe-instances --instance-ids $id > instance-details.json
# TODO get ip


# SSH
# wait
echo "SSH-ing into instance to prepare and run script"
# ssh

# Python from: https://askubuntu.com/questions/101591/how-do-i-install-the-latest-python-2-7-x-or-3-x-on-ubuntu
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
version=2.7.13
cd ~/Downloads/
wget https://www.python.org/ftp/python/$version/Python-$version.tgz
tar -xvf Python-$version.tgz
cd Python-$version
./configure
make
sudo checkinstall

# Dowload & run script
#TODO install git 
mkdir scrape #check path
cd scrape
git clone #url
python src/scraper

# Send logs to right place & logout
scpy #send to right folder
logout

echo #log