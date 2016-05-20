# cmip6-publication-site
new CMDIP6 Publication reporting site

    virtualenv2 env
    source env/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py makemigrations publisher
    python manage.py migrate
    python mangae.py migrate publisher
    python manage.py createsuperuser
     > username:
     > email:
     > password:
     > password:
    python manage.py loaddata
    python manage.py runserver

To prevent unnecessary server load, the network graph reads from a static json file.
Create and update the json file by running the following command:

    python manage.py createjson

It is recommended that this command be set up to run nightly (via a cron job for example).

For development use the following line to start a simple smtp server:

    python -m smtpd -n -c DebuggingServer localhost:1025

Inside of the local_setting.py you will want to set the following values as well:

    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025

Production versions should set the full suite of smtp options according to the mail server being used.