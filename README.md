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

* Setup control machine (but this in a bash script eventually):
```bash
$ wget https://releases.hashicorp.com/terraform/0.8.5/terraform_0.8.5_linux_386.zip
$ sudo apt-get install unzip
$ unzip terraform_0.8.5_linux_386.zip
$ git clone https://github.com/Enturk/Insight-Data-Ops.git
$ sudo mv terraform /usr/local/bin/
$ sudo apt-get update --fix-missing
$ sudo apt-get install python-setuptools -y
$ pip install --upgrade Flask
$ echo "export AIRFLOW_HOME=~/airflow" >> ~/.bashrc
$ echo "export SLUGIFY_USES_TEXT_UNIDECODE=yes" >> ~/.bashrc
$ source ~/.bashrc
$ sudo pip install apache-airflow --user --no-warn-script-location
$ ln -s /home/ubuntu/.local/lib/python2.7/site-packages/airflow/ airflow
$ cd */airflow
$ ./airflow initdb
$ wget http://ipinfo.io/ip -qO - #this just gets your ip for the server...
$ ./airflow webserver -p 8080
$ ./src/newTerraInst.sh
```
* Python script pushes clean data to RDS instance
* RDS checks incoming data and integrates it into appropriate DB
