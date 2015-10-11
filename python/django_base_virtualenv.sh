#!/bin/bash
. ~/.bash_profile

virtualenv_name="$1"
DjangoProjectRoot="$2"

## 1 ## Create Virtual Env
virtualenv $virtualenv_name &&
cd `pwd`/$virtualenv_name ;
source bin/activate;

## 2 ## New Working in Virtual Env Install Django and Create the Base Project
cd `pwd`/$virtualenv_name
pip install Django\>\=1.5


## 3 ## Start Django Project using django-base-templates
django-admin.py startproject --template https://github.com/xenith/django-base-template/zipball/master --extension py,md,rst ${DjangoProjectRoot}
cd  `pwd`/${DjangoProjectRoot}/


## 4 ## Uncomment the DB Used in this Project
sed -e 's/\#MySQL/MySQL/1' -i requirements/compiled.txt

## 5 ## Install the base template reuirements
pip install -r requirements/local.txt
cp ${DjangoProjectRoot}/settings/local-dist.py ${DjangoProjectRoot}/settings/local.py


## End
### Sync
python manage.py syncdb
python manage.py migrate
python manage.py runserver
