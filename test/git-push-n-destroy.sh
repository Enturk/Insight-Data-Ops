#!/bin/bash

# this script is to automate these steps so that I can get the update to the new machine more easily. Airflow will recreate the destroyed instance with the new script.
# if you haven't, follow these steps so you don't need your password to push to github:
# https://stackoverflow.com/questions/8588768/how-do-i-avoid-the-specification-of-the-username-and-password-at-every-git-push

# check args
if [$# != 1]; then
    echo "I need the commit message, in quotes, as an argument"
    exit
fi

# push to github
cd ~/Insight-Data-Ops/
git add .
git commit -m "$1"
git push

# DESTROY MARS!
cd tools/terraform/
terraform destroy -auto-approve
