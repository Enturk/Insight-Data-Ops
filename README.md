# Insight-Data-Ops
This is the project that I worked on during my fellowship with Insight Data in NY. The goal is to be able to automagically spin up and spin down instances in AWS that do some data scraping. Broad view is that the control machine copies or creates a new EC2 Terraform instance via Jenkins. The instance, monitored by Airflow, scrapes data from a website (this example uses the current cases listed on the US 9th Circuit Court of Appeals) using BeautifulSoup, puts that data in an RDS, and then spins down or terminates the instance.

# Workflow Overview

A control machine, running Airflow, monitors Terraform, which is currently setup to recreate instances when I update Github and destroy the instances. This recreation works as outlined below: Terraform re-creates an instance, copies over the environment variables, injects a startup script, which in turn sets up the new instance to run the scraping script and pulls it from github. The python script scrapes the data from a court website, and then pushes it to an AWS relational database.

![workflow: Airflow triggers Terraform, which creates a new instance, which pulls the python scraping script from github, the scraping script gets the data from the court website, and pushes it to the AWS relational DB.](https://raw.githubusercontent.com/Enturk/Insight-Data-Ops/master/Insight-Data-Ops_workflow.png)

# Folder Structure
```
.
├── src                       # Source files
│   ├── newTerraInst.sh       # Checks, and if needed creates new instance, and injects scraper_setup in it
│   ├── scraper_setup.sh      # Installation and setup for scraper
│   ├── scraper.py            # Scrapes and pre-processes data and sends it to RDS
├── test                      # Automated tests 
│   ├── git-push-n-destroy.sh # Pushes changed files to github and destroys terraformed instance
│   ├── sources.txt           # List of websites to be scraped
├── tools                     # Tools and utilities
│   ├── airflow               # Airflow directory
│   ├── terraform             # Terraform directory
├── LICENSE
└── README.md
```

# Assumptions (Dependencies)
Tested with Python 2.7.x on Ubuntu 16.04 LTS

# How to get this going:
* As appropriate, produce or download public & secret keys, user info, region & host to .env file (not discussed for security reasons...). Dotenv file format should be: 
```bash
export ws_access_key_id=
export aws_secret_access_key=
export region=
export POSTGRES_HOST=
export POSTGRES_USER=
export POSTGRES_PASSWORD=
```

* Get pem keypair into right place:
```bash
$ mv *.pem ~/.ssh/*.pem
$ chmod 700 ~/.ssh/*.pem
```

* Setup control machine (put this in a bash script eventually):
```bash
$ sudo apt-get update
$ wget https://releases.hashicorp.com/terraform/0.8.5/terraform_0.8.5_linux_386.zip
$ sudo apt-get install unzip
$ unzip terraform_0.8.5_linux_386.zip
$ git clone https://github.com/Enturk/Insight-Data-Ops.git
$ sudo mv terraform /usr/local/bin/
```
* Create tools/terraform/variables.tf with this format:
```bash
# AWS Config
variable "aws_access_key" {
  default = "XXXXXXXXXX" # change to appropriate value
}
variable "aws_secret_key" {
  default = "XXXXXXXXXXXXXXXXXXXXX" # change to appropriate value
}
variable "aws_region" {
  default = "us-east-1" # change to appropriate value
}
variable "postgres_host" {
   default = "XXXXXXXXX.XXXXXXXXXXXX.us-east-1.rds.amazonaws.com" # change to appropriate value
}
variable "postgres_user" {
   default = "XXXXXXX" # change to appropriate value
}
variable "postgres_password" {
   default = "XXXXXXXXXXXXXX" # change to appropriate value
}
```
* Airflow:
```bash
$ sudo apt-get update --fix-missing
$ sudo apt-get install python-setuptools -y
$ pip install --upgrade setuptools --user
$ curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
$ sudo -H python get-pip.py
$ pip install --upgrade Flask --user # get version 0.12.4
$ echo "export AIRFLOW_HOME=~/airflow" >> ~/.bashrc
$ echo "export SLUGIFY_USES_TEXT_UNIDECODE=yes" >> ~/.bashrc
$ source ~/.bashrc
$ sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev # No idea which one makes airflow work...
$ pip install cryptography --user
$ pip install apache-airflow --user
$ pip install apache-airflow[postgres,s3] --user
$ cp ~/Insight-Data-Ops/tools/airflow/airflow.cfg airflow.cfg
$ airflow initdb
$ wget http://ipinfo.io/ip -qO - #this just gets your ip for the server...
$ airflow webserver -p 8080 &
$ airflow scheduler &
```
* Script to create (and destroy) new terraform instance and injects requirements to run scraper:
```bash
$ chmod +x ~/Insight-Data-Ops/src/newTerraInst.sh
$ export PATH=$PATH:~/Insight-Data-Ops/src/ # or appropriate path
$ cd 
$ ./Insight-Data-Ops/src/newTerraInst.sh
```
* Python script pushes clean data to RDS instance
* RDS checks incoming data and integrates it into appropriate DB
