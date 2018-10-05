# Insight-Data-Ops
This is the project that I worked on during my fellowship with Insight Data in NY. The goal is to be able to automagically spin up and spin down instances in AWS that do some data scraping. Broad view is that the control machine copies or creates a new EC2 Terraform instance via Jenkins. The instance, monitored by Airflow, scrapes data from a website (this example uses the current cases listed on the US 9th Circuit Court of Appeals) using BeautifulSoup, puts that data in an RDS, and then spins down or terminates the instance.

# Architecture Solution

# Folder Structure
```
.
├── docs                    # Documentation files (alternatively `doc`)
│   ├── TOC.md              # Table of contents
│   ├── misc.md             # Miscellaneous information
│   ├── schema.md           # Table schemas for your DB
│   ├── usage.md            # Getting started guide
├── src                     # Source files (alternatively `lib` or `app`)
├── test                    # Automated tests (alternatively `spec` or `tests`)
├── tools                   # Tools and utilities
├── LICENSE
└── README.md
```

# Dependencies
Assuming you have Python 2.7.x or 3.6.x

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
