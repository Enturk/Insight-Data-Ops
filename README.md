# Insight-Data-Ops
This is the project that I worked on during my fellowship with Insight Data in NY. The goal is to be able to automagically spin up and spin down instances in AWS that do some data scraping. So, the plan is to 

# TO DO in this Read moi
Intro to business problem that you are trying to solve
Architecture solution that you've made (with picture)

# Folder structure
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
Assuming you have Python 2.7.x

# How to get this going:
* Jenkins:
```bash
$ sudo yum update –y
$ sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins.io/redhat/jenkins.repo
$ sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
$ sudo service jenkins start
```
* Service will start at http://your-server-address:8080
* Terraform:
```bash
$ sudo wget https://releases.hashicorp.com/terraform/0.8.5/terraform_0.8.5_linux_386.zip
$ sudo unzip terraform_0.8.5_linux_386.zip
$ sudo mv terraform /usr/local/bin/
```
* Create Terraform instance
* Install dependencies on Terraform instance:
```bash
$ python get-pip.py --user
$ pip install awscli --upgrade --user
$ sudo apt-get install git
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo easy_install pip
$ sudo pip install BeautifulSoup4
$ sudo pip install boto3 
$ sudo pip install awscli
$ sudo pip install -U python-dotenv
$ sudo pip install psycopg2

```
* Pull git repo to Terraform instance
* Add public & secret keys, user info, region & host to .env file (not in this git)
* Connect Terraform instance to RDS instance
* Start python scraping script
* Python script pushes clean data to RDS instance
* RDS checks incoming data and integrates it into appropriate DB
